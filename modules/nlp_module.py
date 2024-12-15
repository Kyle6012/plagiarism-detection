from transformers import AutoTokenizer, AutoModel
import torch

class TextSimilarityAnalyzer:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze()

    def analyze_text_similarity(self, text1, text2):
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        cosine_sim = torch.nn.functional.cosine_similarity(emb1.unsqueeze(0), emb2.unsqueeze(0)).item()
        return cosine_sim