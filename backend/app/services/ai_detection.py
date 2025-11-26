import os
from typing import Dict, Any

try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

class AIDetectionService:
    def __init__(self, model_name="roberta-base-openai-detector"):
        self.classifier = None
        self.enabled = False
        self.use_external_api = os.getenv("USE_EXTERNAL_AI_DETECTION", "false").lower() == "true"
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Use external API if configured
        if self.use_external_api and self.openai_api_key:
            self.enabled = True
            print("Using external OpenAI API for AI detection")
        # Otherwise use local model (if not on Vercel)
        elif HAS_TRANSFORMERS and not os.getenv("VERCEL"):
            try:
                # We use a pipeline for text classification
                # Note: This will download the model on first run (approx 500MB)
                self.classifier = pipeline("text-classification", model=model_name)
                self.enabled = True
                print("Using local HuggingFace model for AI detection")
            except Exception as e:
                print(f"Failed to load AI detection model: {e}")

    def _detect_with_openai(self, text: str) -> Dict[str, Any]:
        """Detect AI-generated text using OpenAI API (requires GPT-3.5 or higher)"""
        try:
            import openai
            openai.api_key = self.openai_api_key
            
            prompt = f"""Analyze the following text and determine if it was written by AI or a human.
Respond with ONLY a JSON object with two fields:
- "is_ai": true or false
- "confidence": a number between 0 and 1

Text to analyze:
{text[:2000]}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                "is_ai": result.get("is_ai", False),
                "score": result.get("confidence", 0.5),
                "confidence": result.get("confidence", 0.5),
                "label": "AI" if result.get("is_ai") else "Human",
                "message": "Analysis complete (OpenAI API)"
            }
        except Exception as e:
            print(f"Error using OpenAI API: {e}")
            return {
                "is_ai": False,
                "score": 0.0,
                "confidence": 0.0,
                "label": "ERROR",
                "message": f"OpenAI API error: {str(e)}"
            }

    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detects if the text is AI-generated.
        Returns a dictionary with 'is_ai' (bool) and 'score' (float).
        """
        if not self.enabled:
            return {
                "is_ai": False,
                "score": 0.0,
                "confidence": 0.0,
                "label": "UNKNOWN",
                "message": "AI Detection unavailable (Lite Mode or Model missing)"
            }
        
        # Use external API if configured
        if self.use_external_api and self.openai_api_key:
            return self._detect_with_openai(text)

        # Use local model
        if not self.classifier:
            return {
                "is_ai": False,
                "score": 0.0,
                "confidence": 0.0,
                "label": "UNKNOWN",
                "message": "Local model not available"
            }

        # Truncate text to 512 tokens approx (simple char limit for safety)
        # Real implementation should handle chunking
        truncated_text = text[:2000] 

        try:
            result = self.classifier(truncated_text)[0]
            # result looks like: {'label': 'Fake', 'score': 0.99} or {'label': 'Real', 'score': 0.99}
            
            label = result['label']
            score = result['score']
            
            # 'Fake' usually means AI-generated in these models
            is_ai = label == 'Fake'
            
            return {
                "is_ai": is_ai,
                "score": score if is_ai else (1 - score), # Normalize to AI probability
                "confidence": score,
                "label": label,
                "message": "Analysis complete (Local Model)"
            }
        except Exception as e:
            print(f"Error during AI detection: {e}")
            return {
                "is_ai": False,
                "score": 0.0,
                "confidence": 0.0,
                "label": "ERROR",
                "message": str(e)
            }
