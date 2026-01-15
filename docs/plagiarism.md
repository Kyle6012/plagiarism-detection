# Plagiarism Detection Algorithm

## Overview

The plagiarism detection system uses **semantic similarity analysis** at the chunk level, powered by Sentence-BERT embeddings and cosine similarity scoring.

## Algorithm Flow

```
Document A                    Document B
    ↓                             ↓
┌─────────────┐            ┌─────────────┐
│  Chunking   │            │  Chunking   │
└──────┬──────┘            └──────┬──────┘
       │                          │
   [500 chars]                [500 chars]
   50 overlap                 50 overlap
       │                          │
       ↓                          ↓
┌─────────────┐            ┌─────────────┐
│  Embedding  │            │  Embedding  │
│   (SBERT)   │            │   (SBERT)   │
└──────┬──────┘            └──────┬──────┘
       │                          │
       └──────────┬───────────────┘
                  ↓
         ┌────────────────┐
         │ Cosine Similarity│
         │  (Chunk × Chunk) │
         └────────┬─────────┘
                  ↓
            ┌──────────┐
            │Score > 0.75?│
            └─────┬──────┘
                  ↓
            [Store Match]
                  ↓
         ┌─────────────────┐
         │ Overall Score:  │
         │ Σ(matches) / N  │
         └─────────────────┘
```

## Step-by-Step

### 1. Text Chunking

**Implementation:** `EmbeddingService.chunk_text()`

```python
chunk_size = 500  # characters
overlap = 50      # characters
```

**Why Chunking?**
- **Granularity:** Detect localized plagiarism (e.g., a single paragraph)
- **Context:** Preserve semantic meaning within each chunk
- **Scalability:** Process long documents without hitting model limits

**Trade-offs:**
- Too small → Loss of context, noisy matches
- Too large → Miss localized plagiarism
- 500 chars ≈ 3-5 sentences, empirically good balance

### 2. Embedding Generation

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

**Specifications:**
- **Dimensions:** 384
- **Max Sequence:** 256 tokens (~512 chars)
- **Speed:** ~1000 sentences/sec on CPU
- **Quality:** Optimized for semantic search

**Why SBERT?**
- Pre-trained on paraphrase detection tasks
- Captures semantic similarity, not just lexical overlap
- Fast inference (vs full transformer models)

### 3. Similarity Calculation

**Metric:** Cosine Similarity

```python
similarity = dot(vec_a, vec_b) / (||vec_a|| * ||vec_b||)
```

**Range:** -1 to 1 (we use 0 to 1 after normalization)

**Interpretation:**
- `1.0` → Identical semantic meaning
- `0.75-1.0` → High similarity (plagiarism threshold)
- `0.5-0.75` → Moderate similarity (paraphrasing)
- `< 0.5` → Low similarity (different content)

### 4. Match Detection

**Threshold:** 0.75

For each chunk in Document A:
1. Compare against all chunks in Document B
2. Select best match (highest score)
3. If score > 0.75 → **MATCH**

**Why 0.75?**
- Empirically validated to reduce false positives
- Strict enough to avoid matching unrelated content
- Lenient enough to catch paraphrased plagiarism

### 5. Overall Score Calculation

```python
overall_score = sum(matched_chunk_scores) / total_chunks_in_A
```

**Interpretation:**
- `0.8-1.0` → Very high plagiarism (80%+ of document matches)
- `0.5-0.8` → Significant plagiarism
- `0.2-0.5` → Moderate overlap (could be coincidence/common references)
- `< 0.2` → Low/no plagiarism

## Limitations

### False Positives

**Common Phrases:**
- Technical jargon (e.g., "machine learning model")
- Standard academic language (e.g., "the results show that")
- **Mitigation:** Threshold tuning, exclude common n-grams (future work)

**Domain-Specific Vocabulary:**
- Legal documents, medical texts have repetitive language
- **Mitigation:** Domain-specific models (future work)

### False Negatives

**Synonym Substitution:**
- SBERT is good but not perfect at catching all paraphrases
- **Mitigation:** Ensemble with lexical overlap metrics (future work)

**Structural Plagiarism:**
- Copying idea structure without copying text
- **Limitation:** Our system doesn't detect this

**Cross-Lingual Plagiarism:**
- Translation-based plagiarism
- **Limitation:** Requires multilingual models (future work)

### Performance Constraints

**Complexity:** O(N × M) where N, M = chunk counts

**Scalability Issues:**
- 100-page document × 100-page document = ~20,000 comparisons
- **Mitigation:** Use FAISS or pgvector for approximate nearest neighbor search

## Comparison Scope

**Important:** This system **only** compares documents within the same uploaded batch.

**It does NOT:**
- Search the internet for sources
- Check against a global plagiarism database
- Compare with previous batches (unless explicitly configured)

**Why Batch-Only?**
- Privacy: User data stays isolated
- Performance: Avoid massive corpus comparisons
- Scope: Designed for academic course/assignment checking

## Future Enhancements

### Planned Improvements

1. **N-gram Overlap:** Add lexical similarity for exact-match detection
2. **FAISS Integration:** Speed up chunk search with approximate NN
3. **External Corpus:** Option to check against public datasets (arXiv, Wikipedia)
4. **Citation Detection:** Exclude properly cited passages
5. **Paraphrase Quality:** More sophisticated paraphrase detection models

### Research Directions

- **Graph-based Similarity:** Model document structure
- **Cross-lingual Detection:** Multilingual embeddings
- **Code Plagiarism:** Specialized AST-based comparison for source code

## References

- **Sentence-BERT:** [Reimers & Gurevych, 2019](https://arxiv.org/abs/1908.10084)
- **Cosine Similarity:** Standard metric in information retrieval
- **Chunking Strategy:** Inspired by long-document summarization techniques
