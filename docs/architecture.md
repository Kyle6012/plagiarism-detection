# System Architecture

## Overview

This plagiarism and AI-generated content detection system is built with a **production-grade, auditable architecture** that supports multiple inference backends with explicit provider selection.

## High-Level Architecture

```
┌─────────────────┐
│  React Frontend │ (Vite, TypeScript, TailwindCSS)
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Backend│ (Python 3.11+, Async)
└────────┬────────┘
         │
    ┌────┴─────────────────┬───────────────┬──────────────┐
    ▼                      ▼               ▼              ▼
┌─────────┐          ┌──────────┐    ┌─────────┐   ┌──────────┐
│PostgreSQL│          │  Redis   │    │  MinIO  │   │ External │
│+pgvector │          │(Celery)  │    │(Storage)│   │   APIs   │
└──────────┘          └──────────┘    └─────────┘   └──────────┘
                                                     OpenAI/Together
```

## Core Components

### 1. Provider Router (`app/core/provider_router.py`)

**Responsibility:** Central routing logic for AI detection inference.

- **Validates** provider availability (API keys, local model status)
- **Routes** requests to Local/OpenAI/Together backends
- **Logs** all provider usage for audit trails
- **Fails explicitly** when provider is misconfigured

**Design Principles:**
- No silent fallbacks
- No implicit provider switching
- All decisions are logged and traceable

### 2. AI Detection Service (`app/services/ai_detection.py`)

**Capabilities:**
- **Local Model**: HuggingFace Transformers (`roberta-base-openai-detector`)
- **OpenAI API**: GPT-3.5-turbo for classification
- **Together API**: Mixtral-8x7B for classification

**Output Schema:**
```python
{
    "is_ai": bool,
    "score": float,        # 0.0 (Human) to 1.0 (AI)
    "confidence": float,   # Distance from threshold
    "label": str,          # "Likely AI" | "Likely Human"
    "provider": str,       # "local" | "openai" | "together"
    "details": dict        # Provider-specific metadata
}
```

**Calibration:**
- Confidence calculated as `abs(score - 0.5) * 2` (0-1 range)
- Chunks limited to 20 to prevent OOM
- External APIs receive truncated text (4000 chars)

### 3. Plagiarism Service (`app/services/plagiarism.py`)

**Algorithm:**
1. **Chunking:** Split documents into overlapping chunks (500 chars, 50 overlap)
2. **Embedding:** Generate SBERT embeddings for each chunk
3. **Comparison:** O(N*M) chunk-to-chunk similarity via cosine distance
4. **Aggregation:** Sum matched chunk scores / total chunks in source

**Output Schema:**
```python
{
    "score": float,           # Overall plagiarism score
    "matches": [              # Detailed chunk matches
        {
            "source_chunk": str,
            "target_chunk": str,
            "score": float,
            "source_index": int,
            "target_index": int
        }
    ],
    "details": {
        "chunks_a": int,
        "chunks_b": int
    }
}
```

**Threshold:** Chunks with >0.75 similarity are considered matches.

### 4. API Design (V1)

**Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/analyze` | POST | Unified analysis (files/text) |
| `/v1/ai-detection` | POST | Direct AI check for text |
| `/v1/batches/{id}/results` | GET | Detailed batch results |

**Request Flow:**
1. User uploads files + selects provider/options
2. Files → MinIO storage
3. Batch → PostgreSQL (queued)
4. Celery task → background processing
5. Results → PostgreSQL (with JSONB details)
6. Frontend polls for results

### 5. Database Schema

**Key Tables:**

```sql
-- Batches
CREATE TABLE batches (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    total_docs INT,
    status VARCHAR(50),
    analysis_type VARCHAR(50)
);

-- Documents
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    batch_id UUID REFERENCES batches(id),
    filename VARCHAR(255),
    text_content TEXT,
    embedding VECTOR(384),  -- SBERT embedding
    ai_score FLOAT,
    is_ai_generated BOOLEAN
);

-- Comparisons
CREATE TABLE comparisons (
    id UUID PRIMARY KEY,
    doc_a UUID REFERENCES documents(id),
    doc_b UUID REFERENCES documents(id),
    similarity FLOAT,
    matches JSON  -- Detailed chunk matches
);
```

## Security Considerations

### Current Implementation
✅ JWT-based authentication  
✅ User-scoped batch access  
✅ Provider validation  
✅ Explicit API key checks  

### Missing (Production TODO)
⚠️ Rate limiting on analysis endpoints  
⚠️ File size/type validation (implemented but not strict)  
⚠️ CSRF protection  
⚠️ Input sanitization for text fields  

## Scalability

### Current Bottlenecks
1. **Batch Processing:** O(N²) comparison within batch
2. **Embeddings:** Sequential chunk encoding
3. **Database:** No pagination on results endpoint

### Scaling Strategies
1. **Use FAISS** or pgvector for chunk similarity search (vs brute-force)
2. **Batch encode** chunks in parallel (GPU acceleration)
3. **Implement pagination** with cursor-based results
4. **Horizontal Celery workers** for concurrent batch processing

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React | 18.2 |
| Build Tool | Vite | 5.0 |
| Styling | TailwindCSS | 4.1 |
| Backend | FastAPI | 0.111+ |
| Database | PostgreSQL | 15 |
| Vector Extension | pgvector | 0.2 |
| Task Queue | Celery | 5.3 |
| Cache/Broker | Redis | 5.0 |
| Storage | MinIO | 7.1 |
| ML Framework | Transformers | 4.35+ |
| Embeddings | Sentence-Transformers | 2.2+ |

## Deployment Architecture

### Development
```
docker-compose up --build
```

### Production (Recommended)
- **Frontend:** Vercel/Netlify (static hosting)
- **Backend:** Kubernetes with auto-scaling
- **Database:** Managed PostgreSQL (AWS RDS, Google Cloud SQL)
- **Storage:** S3-compatible object storage
- **Workers:** Celery on dedicated pods with GPU

## Monitoring & Observability

**Implemented:**
- Structured logging via `loguru`
- Prometheus metrics endpoint
- Provider usage logging

**Recommended:**
- Sentry for error tracking
- Grafana dashboards for metrics
- OpenTelemetry for distributed tracing
