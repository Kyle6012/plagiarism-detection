# Provider Comparison Guide

## Overview

The system supports three AI detection providers. This document compares their characteristics to help you choose the right one for your use case.

## Quick Comparison

| Feature | Local Model | OpenAI API | Together API |
|---------|------------|------------|--------------|
| **Privacy** | ✅ Full | ❌ Data sent externally | ❌ Data sent externally |
| **Cost** | ✅ Free | 💰 ~$0.002/request | 💰 ~$0.001/request |
| **Speed** | ✅ Fast (local) | ⚡ Very fast (API) | ⚡ Very fast (API) |
| **Accuracy** | ⭐⭐⭐⭐ ~85% | ⭐⭐⭐⭐⭐ ~90% | ⭐⭐⭐⭐ ~88% |
| **Setup** | ✅ Zero config | 🔑 Requires API key | 🔑 Requires API key |
| **Dependencies** | 📦 transformers, torch | 📦 openai SDK | 📦 openai SDK |
| **Model Age** | Trained on GPT-2/3 | Current GPT models | Open-source models |

## Detailed Breakdown

### Local Model (Recommended Default)

**Model:** `roberta-base-openai-detector`

#### Pros
- **Privacy-First:** Text never leaves your infrastructure
- **No Rate Limits:** Unlimited usage
- **Offline Capable:** Works without internet
- **Free:** No API costs
- **Fast:** ~100 texts/second on CPU

#### Cons
- **Lower Accuracy:** ~85% on GPT-3.5+ text
- **Model Age:** Trained on older AI models
- **Resource Usage:** Requires ~500MB RAM per worker

#### Best For
- Privacy-sensitive environments (GDPR, FERPA compliance)
- High-volume processing
- Cost-constrained deployments
- Offline or air-gapped systems

#### Configuration

```bash
# No configuration needed, works out of the box
# Model downloads automatically on first use (~500MB)
```

---

### OpenAI API

**Model:** GPT-3.5-turbo (classifier mode)

#### Pros
- **Highest Accuracy:** ~90% on modern AI text
- **Self-Supervised:** GPT detecting GPT
- **Zero Local Resources:** Minimal memory footprint
- **Always Updated:** Benefits from OpenAI model improvements

#### Cons
- **Privacy Concerns:** Text sent to OpenAI servers
- **API Costs:** ~$0.002 per text analyzed
- **Rate Limits:** 3,500 requests/min (tier-dependent)
- **Internet Required:** No offline mode

#### Best For
- Maximum accuracy requirements
- Low-volume use cases
- Well-funded projects
- Non-sensitive text

#### Configuration

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
```

**Estimated Costs:**
- 100 documents/day: ~$6/month
- 1,000 documents/day: ~$60/month
- 10,000 documents/day: ~$600/month

---

### Together API

**Model:** Mixtral-8x7B-Instruct

#### Pros
- **Open-Source Model:** Transparent architecture
- **Lower Cost:** ~50% cheaper than OpenAI
- **Good Accuracy:** ~88% on modern AI text
- **Faster:** Often lower latency than OpenAI

#### Cons
- **Privacy Concerns:** Text sent to Together AI servers
- **API Dependency:** Requires internet
- **Less Established:** Newer provider vs OpenAI

#### Best For
- Cost-conscious external API usage
- Open-source preference
- Good accuracy without OpenAI pricing

#### Configuration

```bash
# .env
TOGETHER_API_KEY=your-together-key-here
```

**Estimated Costs:**
- 100 documents/day: ~$3/month
- 1,000 documents/day: ~$30/month
- 10,000 documents/day: ~$300/month

## Provider Selection Strategy

### Decision Tree

```
Start
  │
  ├─ Privacy Required? ──YES──> Local Model
  │
  ├─ Budget < $50/mo? ──YES──> Local Model or Together
  │
  ├─ Need >90% accuracy? ──YES──> OpenAI API
  │
  └─ Default ──────────────────> Local Model
```

### Use Case Recommendations

#### Academic Institution (K-12)
- **Primary:** Local Model
- **Reason:** FERPA compliance, student privacy, cost

#### University Research
- **Primary:** Together API
- **Fallback:** Local Model
- **Reason:** Balance of accuracy and cost

#### Enterprise Compliance
- **Primary:** Local Model (on-premise)
- **Reason:** Data sovereignty, audit requirements

#### Startup/Small Business
- **Primary:** Together API
- **Reason:** No infrastructure overhead, good accuracy/cost ratio

#### High-Stakes Assessment
- **Primary:** OpenAI API
- **Secondary:** Manual review
- **Reason:** Maximum accuracy, human oversight

## Multi-Provider Strategy

### Ensemble Detection

**Approach:** Run multiple providers and compare results

```python
local_result = detect(text, provider="local")
openai_result = detect(text, provider="openai")

if abs(local_result.score - openai_result.score) > 0.3:
    # Disagreement → flag for manual review
    flag_for_review()
else:
    # Consensus → higher confidence
    final_score = mean([local_result.score, openai_result.score])
```

**Benefits:**
- Increased confidence
- Reduces false positives
- Catches edge cases

**Drawbacks:**
- 2x cost (if using paid APIs)
- Slower (sequential calls)

### Tiered Detection

**Approach:** Cheap first-pass, expensive confirmation

```python
# Step 1: Local model (fast, free)
local_score = detect(text, provider="local")

# Step 2: If uncertain, use premium API
if 0.4 < local_score < 0.6:
    final_score = detect(text, provider="openai")
else:
    final_score = local_score
```

**Benefits:**
- Cost optimization (only pay for uncertain cases)
- Fast for clear-cut cases
- Best of both worlds

## Technical Implementation

### Switching Providers

**Frontend (User Selection):**
```tsx
<select value={provider} onChange={(e) => setProvider(e.target.value)}>
  <option value="local">Local Model (Free)</option>
  <option value="openai">OpenAI (Premium)</option>
  <option value="together">Together AI (Mid-tier)</option>
</select>
```

**Backend (Provider Router):**
```python
from app.core.provider_router import ProviderRouter

router = ProviderRouter()
validated_provider = router.validate_provider(user_choice)
# Explicit validation, no silent fallbacks
```

### Error Handling

**Local Model Failure:**
```python
try:
    result = detect(text, provider="local")
except ModelNotLoadedError:
    return {"error": "Local model not available, choose external provider"}
```

**API Failure:**
```python
try:
    result = detect(text, provider="openai")
except APIKeyMissingError:
    return {"error": "OpenAI API key not configured"}
except RateLimitError:
    return {"error": "API rate limit exceeded, try again later"}
```

## Cost Optimization Tips

1. **Batch Processing:** Group multiple texts per API call (if provider supports)
2. **Caching:** Store results, avoid re-analyzing same text
3. **Thresholds:** Only use premium API for high-risk scenarios
4. **Hybrid Strategy:** Local for bulk, API for spot-checks

## Future Provider Additions

**Planned:**
- Anthropic Claude API
- Google Gemini API
- Custom Self-Hosted Models

**Criteria for Addition:**
- Documented accuracy benchmarks
- Reasonable pricing
- API stability
- User demand

## References

- [OpenAI Pricing](https://openai.com/pricing)
- [Together AI Pricing](https://www.together.ai/pricing)
- [RoBERTa GPT-2 Detector](https://huggingface.co/roberta-base-openai-detector)
