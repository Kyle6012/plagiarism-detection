import numpy as np
from transformers import ViTModel, ViTFeatureExtractor
from PIL import Image
import torch
import imagehash

class ImageAnalyzer:
    def __init__(self):
        self.feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224")
        self.model = ViTModel.from_pretrained("google/vit-base-patch16-224")

    def extract_image_features(self, image_path):
        image = Image.open(image_path)
        inputs = self.feature_extractor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Assume we take the mean of the last hidden state for simplicity
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def get_image_hash(self, image_path):
        # Optionally keep the perceptual hashing if needed
        img = Image.open(image_path)
        return str(imagehash.phash(img))