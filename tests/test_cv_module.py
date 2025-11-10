import unittest
import os
import numpy as np
from PIL import Image
from modules.cv_module import ImageAnalyzer

class TestImageAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = ImageAnalyzer()
        self.test_image_path = "tests/dummy_image.png"

        # Create a dummy image for testing
        if not os.path.exists(self.test_image_path):
            img = Image.new('RGB', (100, 100), color = 'red')
            img.save(self.test_image_path)

    def test_feature_extraction_dimensionality(self):
        features = self.analyzer.extract_image_features(self.test_image_path)
        self.assertEqual(features.shape[0], 768)

    def test_image_hash_format(self):
        image_hash = self.analyzer.get_image_hash(self.test_image_path)
        self.assertIsInstance(image_hash, str)

if __name__ == "__main__":
    unittest.main()
