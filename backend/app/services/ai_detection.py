import os
import json
import logging
from typing import Dict, Any, Optional

from app.core.provider_router import ProviderRouter, ProviderType

# Configure logging
logger = logging.getLogger(__name__)

class AIDetectionService:
    def __init__(self):
        self.router = ProviderRouter()
        self.classifier = None
        self._load_local_model()

    def _load_local_model(self):
        """Lazy load the local model to save resources if not used."""
        if self.classifier is None and self.router.local_model_available:
            try:
                from transformers import pipeline
                # Use a standard, reliable model for AI detection
                model_name = "roberta-base-openai-detector" 
                self.classifier = pipeline("text-classification", model=model_name)
                logger.info(f"Local AI detection model '{model_name}' loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load local AI model: {e}")
                self.classifier = None

    def detect(self, text: str, provider: str = ProviderType.LOCAL, threshold: float = 0.5) -> Dict[str, Any]:
        """
        Detects if text is AI-generated using the specified provider.
        
        Args:
            text: The text to analyze.
            provider: 'local', 'openai', or 'together'.
            threshold: Confidence threshold for 'AI' label (default 0.5).
            
        Returns:
            Dict containing 'is_ai', 'score', 'confidence', 'provider', 'details'.
        """
        try:
            # Validate provider
            validated_provider = self.router.validate_provider(provider)
            self.router.log_usage(validated_provider, "ai_detection", {"text_length": len(text)})

            if validated_provider == ProviderType.LOCAL:
                return self._detect_local(text, threshold)
            elif validated_provider == ProviderType.OPENAI:
                return self._detect_external(text, ProviderType.OPENAI, threshold)
            elif validated_provider == ProviderType.TOGETHER:
                return self._detect_external(text, ProviderType.TOGETHER, threshold)
            
        except ValueError as e:
            logger.error(f"Provider validation failed: {e}")
            return self._error_response(str(e))
        except Exception as e:
            logger.exception(f"AI detection failed: {e}")
            return self._error_response(f"Internal error: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the AI detection service is operational."""
        return {
            "status": "healthy" if self.classifier is not None else "unavailable",
            "local_model_loaded": self.classifier is not None,
            "external_providers": {
                "openai": self.router.openai_api_key is not None,
                "together": self.router.together_api_key is not None
            }
        }

    def _detect_local(self, text: str, threshold: float) -> Dict[str, Any]:
        """Run detection using local HuggingFace model."""
        if not self.classifier:
            self._load_local_model()
            if not self.classifier:
                return self._error_response("Local model unavailable")

        # Chunking for long text (simple overlap)
        chunk_size = 512 # Token approximation
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        
        # Limit chunks to prevent OOM/timeout on massive files
        chunks = chunks[:20] 
        
        results = []
        try:
            for chunk in chunks:
                # Truncate to 512 chars roughly to be safe for model
                res = self.classifier(chunk[:512])[0]
                results.append(res)
        except Exception as e:
            return self._error_response(f"Model inference failed: {e}")

        if not results:
            return self._error_response("No text to analyze")

        # Aggregate scores
        # Model returns label='Fake' (AI) or 'Real' (Human)
        # We want probability of AI
        ai_probs = []
        for res in results:
            score = res['score']
            if res['label'] == 'Fake':
                ai_probs.append(score)
            else:
                ai_probs.append(1 - score)
        
        avg_ai_score = sum(ai_probs) / len(ai_probs)
        is_ai = avg_ai_score > threshold
        
        # Calculate confidence (distance from 0.5, normalized to 0-1 range)
        # If score is 0.9, confidence is high. If 0.51, confidence is low.
        confidence = (abs(avg_ai_score - 0.5) * 2)

        return {
            "is_ai": is_ai,
            "score": round(avg_ai_score, 4),
            "confidence": round(confidence, 4),
            "label": "Likely AI" if is_ai else "Likely Human",
            "provider": ProviderType.LOCAL,
            "details": {
                "chunks_analyzed": len(results),
                "model": "roberta-base-openai-detector"
            }
        }

    def _detect_external(self, text: str, provider: str, threshold: float) -> Dict[str, Any]:
        """Run detection using OpenAI or Together API."""
        from openai import OpenAI
        
        api_key = self.router.get_api_key(provider)
        base_url = None
        model = "gpt-3.5-turbo" # Default
        
        if provider == ProviderType.TOGETHER:
            base_url = "https://api.together.xyz/v1"
            model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        prompt = f"""Analyze the following text for AI-generated content.
        Respond with a JSON object containing:
        - "score": A float between 0.0 (Human) and 1.0 (AI) representing the probability of being AI-generated.
        - "reasoning": A brief explanation.
        
        Text:
        {text[:4000]}""" # Truncate to fit context window

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert AI detection system. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            ai_score = float(result.get("score", 0.5))
            is_ai = ai_score > threshold
            confidence = (abs(ai_score - 0.5) * 2)
            
            return {
                "is_ai": is_ai,
                "score": round(ai_score, 4),
                "confidence": round(confidence, 4),
                "label": "Likely AI" if is_ai else "Likely Human",
                "provider": provider,
                "details": {
                    "reasoning": result.get("reasoning", "No reasoning provided"),
                    "model": model
                }
            }
            
        except Exception as e:
            logger.error(f"External API error ({provider}): {e}")
            return self._error_response(f"External provider error: {str(e)}")

    def _error_response(self, message: str) -> Dict[str, Any]:
        return {
            "is_ai": False,
            "score": 0.0,
            "confidence": 0.0,
            "label": "Error",
            "provider": "unknown",
            "details": {"error": message}
        }
