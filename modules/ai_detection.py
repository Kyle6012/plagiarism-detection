from transformers import AutoTokenizer as AT, AutoModelForSequenceClassification as AMFSC
import torch

model_name = "roberta-base-openai-detector"

def load_ai_detection_model():
    tokenizer = AT.from_pretrained(model_name)
    model = AMFSC.from_pretrained(model_name)
    return tokenizer, model
    
def detect_ai_generated_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)
    scores = torch.softmax(outputs.logits, dim=1)
    return scores[0][1].item()  # Assuming class 1 indicates AI-generated
