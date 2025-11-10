import unittest
from modules.nlp_module import TextSimilarityAnalyzer

class TestTextSimilarityAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextSimilarityAnalyzer()

    def test_embedding_dimensionality(self):
        text = "This is a sample sentence for testing."
        embedding = self.analyzer.get_embedding(text)
        self.assertEqual(embedding.shape[0], 384)

    def test_similarity_score_range(self):
        text1 = "The cat sat on the mat."
        text2 = "A feline was resting on the rug."
        similarity = self.analyzer.analyze_text_similarity(text1, text2)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)

if __name__ == "__main__":
    unittest.main()
