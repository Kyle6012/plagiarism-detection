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
        self.together_api_key = os.getenv("TOGETHER_API_KEY")
        
        # Use external API if configured
        if self.use_external_api and (self.openai_api_key or self.together_api_key):
            self.enabled = True
            print("Using external API (OpenAI/Together) for AI detection")
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
        """Detect AI-generated text using OpenAI API or Together API"""
        try:
            from openai import OpenAI
            
            client = None
            model = "gpt-3.5-turbo"
            provider = "OpenAI"
            
            if self.together_api_key:
                client = OpenAI(
                    api_key=self.together_api_key,
                    base_url="https://api.together.xyz/v1"
                )
                model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
                provider = "Together API"
            elif self.openai_api_key:
                client = OpenAI(api_key=self.openai_api_key)
            else:
                raise ValueError("No API key found for OpenAI or Together API")
            
            prompt = f"""Analyze the following text and determine if it was written by AI or a human.
Respond with ONLY a JSON object with two fields:
- "is_ai": true or false
- "confidence": a number between 0 and 1
            
Text to analyze:
{text[:2000]}"""
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            
            import json
            content = response.choices[0].message.content
            # Handle potential markdown code block wrapping
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
                
            result = json.loads(content.strip())
            
            return {
                "is_ai": result.get("is_ai", False),
                "score": result.get("confidence", 0.5),
                "confidence": result.get("confidence", 0.5),
                "label": "AI" if result.get("is_ai") else "Human",
                "message": f"Analysis complete ({provider})"
            }
        except Exception as e:
            print(f"Error using External API: {e}")
            return {
                "is_ai": False,
                "score": 0.0,
                "confidence": 0.0,
                "label": "ERROR",
                "message": f"External API error: {str(e)}"
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
        if self.use_external_api and (self.openai_api_key or self.together_api_key):
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

        # Chunk text for better detection on long documents
        chunk_size = 1000
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        
        try:
            results = []
            for chunk in chunks[:5]: # Limit to first 5 chunks for performance
                res = self.classifier(chunk)[0]
                results.append(res)
            
            if not results:
                return {"is_ai": False, "score": 0.0, "confidence": 0.0, "label": "UNKNOWN", "message": "No text to analyze"}

            # Aggregate results (average AI probability)
            ai_scores = []
            for res in results:
                label = res['label']
                score = res['score']
                # 'Fake' usually means AI-generated in these models
                is_ai_chunk = label == 'Fake'
                ai_scores.append(score if is_ai_chunk else (1 - score))
            
            avg_ai_score = sum(ai_scores) / len(ai_scores)
            is_ai = avg_ai_score > 0.5
            
            return {
                "is_ai": is_ai,
                "score": avg_ai_score,
                "confidence": max(ai_scores) if is_ai else (1 - min(ai_scores)),
                "label": "Fake" if is_ai else "Real",
                "message": f"Analysis complete ({len(results)} chunks analyzed)"
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
