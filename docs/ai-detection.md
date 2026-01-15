# AI-Generated Content Detection

## Overview

This system detects AI-generated text using machine learning classifiers that analyze linguistic patterns characteristic of large language models (GPT-3, GPT-4, etc.).

## Detection Methods

### Local Model (Default)

**Model:** `roberta-base-openai-detector`

**Architecture:**
- Base: RoBERTa (125M parameters)
- Training: Fine-tuned on GPT-2/GPT-3 outputs
- Output: Binary classification (Real/Fake)

**Performance Characteristics:**
- **Speed:** ~100 texts/second on CPU
- **Accuracy:** ~95% on GPT-2, ~85% on GPT-3.5 (based on published benchmarks)
- **Privacy:** Fully local, no data leaves your server

**Inference Process:**
1. Chunk text into 512-character segments (max 20 chunks)
2. Run each chunk through classifier
3. Aggregate scores via averaging
4. Calculate confidence based on variance

### External Providers

#### OpenAI API

**Model:** GPT-3.5-turbo (meta-classification)

**Process:**
```
User Text → GPT-3.5 Prompt → Classification JSON
```

**Advantages:**
- High accuracy on modern AI text
- Self-supervised (GPT detecting GPT)

**Disadvantages:**
- API costs (~$0.002 per request)
- Data sent to OpenAI
- Requires API key

#### Together API

**Model:** Mixtral-8x7B-Instruct

**Process:** Similar to OpenAI, uses open-source model

**Advantages:**
- Competitive accuracy
- Open-source model
- Often cheaper than OpenAI

**Disadvantages:**
- Still external API
- Requires API key

## Output Schema

```json
{
  "is_ai": true,
  "score": 0.87,           // Probability of AI (0-1)
  "confidence": 0.74,      // Distance from threshold
  "label": "Likely AI",
  "provider": "local",
  "details": {
    "chunks_analyzed": 5,
    "model": "roberta-base-openai-detector"
  }
}
```

## Confidence Calculation

```python
confidence = abs(score - 0.5) * 2
```

**Examples:**
- Score = 0.9 → Confidence = 0.8 (high confidence AI)
- Score = 0.51 → Confidence = 0.02 (low confidence, near threshold)
- Score = 0.1 → Confidence = 0.8 (high confidence Human)

**Interpretation:**
- `> 0.7` → High confidence
- `0.3-0.7` → Moderate confidence
- `< 0.3` → Low confidence (inconclusive)

## Known Limitations

### ⚠️ High False Positive Risk

**ESL (English as Second Language) Writers:**
- Non-native English often triggers AI detection
- Reason: Simple sentence structure, limited vocabulary
- **Impact:** Serious risk of false accusations

**Formal Writing:**
- Overly formal or technical language
- Academic templates
- **Impact:** Legitimate work flagged as AI

**Mitigation:**
- Use confidence scores, not binary labels
- Manual review required
- Provide context to reviewers

### Model Limitations

**Training Data Bias:**
- Trained on GPT-2/early GPT-3 outputs
- May underperform on GPT-4, Claude, etc.
- Constantly evolving AI landscape

**Adversarial Attacks:**
- Minor edits can fool detectors
- Paraphrasing tools bypass detection
- **No detector is foolproof**

### Context Matters

**Mixed Content:**
- Human outline + AI elaboration
- AI-assisted editing
- **System averages scores → misses nuance**

**Topic Dependence:**
- Some topics (e.g., technical documentation) naturally resemble AI
- Creative writing vs factual writing have different baselines

## Best Practices

### For Educators

1. **Use as a screening tool only**
   - Red flags, not verdicts
   - Always require human review

2. **Review low-confidence cases**
   - Scores near 0.5 are inconclusive
   - Request additional evidence

3. **Consider context**
   - Student's prior work
   - Deadline pressure
   - Assignment type

### For Administrators

1. **Transparent disclosure**
   - Inform users that detection is probabilistic
   - Publish false positive rates

2. **Appeals process**
   - Allow contested results
   - Manual expert review

3. **Regular auditing**
   - Track false positive/negative rates
   - Update models as AI evolves

## Technical Details

### Chunking Strategy

**Why Chunk?**
- Models have token limits
- Analyze long documents incrementally

**Current Implementation:**
- Max 20 chunks
- First 512 characters per chunk
- Prevents OOM on huge files

**Trade-off:**
- May miss patterns in later sections
- **Future:** Sliding window with attention pooling

### Aggregation Logic

**Current:** Simple averaging

```python
ai_scores = [chunk_score for chunk in chunks]
overall_score = mean(ai_scores)
```

**Limitation:** Assumes uniform distribution

**Future Enhancement:**
```python
# Weighted by chunk position
weights = [1.0, 0.9, 0.8, ...]  # Introduction has more weight
overall_score = weighted_mean(ai_scores, weights)
```

## Comparison with Other Tools

| Tool | Accuracy | Privacy | Cost | Speed |
|------|----------|---------|------|-------|
| **Our Local** | ~85% | Full | Free | Fast |
| GPTZero | ~90% | Partial | $10/mo | Medium |
| Turnitin AI | ~95%* | None | $$$ | Slow |
| OpenAI API | ~90% | None | $0.002/req | Fast |

*Claimed by vendor, not independently verified

## Ethical Considerations

### Academic Integrity

**Concern:** Over-reliance on automated detection

**Position:** 
- Tools are assistive, not definitive
- Human judgment irreplaceable
- Context and intent matter

### Bias and Fairness

**Documented Biases:**
- Non-native speakers
- Neurodivergent writers
- Certain dialects/sociolects

**Mitigation Efforts:**
- Confidence thresholds
- Manual review requirement
- Ongoing bias audits

### Privacy

**Our Stance:**
- Local models preferred
- External APIs opt-in only
- Clear user consent required

## Future Work

### Model Improvements

1. **Fine-tuning on GPT-4 outputs**
2. **Multi-model ensemble** (combine local + external)
3. **Explainability features** (highlight suspicious passages)

### Feature Additions

1. **Per-paragraph analysis** (not just document-level)
2. **Temporal analysis** (detect sudden writing style changes)
3. **Source attribution** (which AI model likely generated it)

## References

- [Detecting GPT-2 Generated Text](https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text/)
- [RoBERTa Architecture](https://arxiv.org/abs/1907.11692)
- [Limitations of AI Detectors](https://arxiv.org/abs/2303.13408)
