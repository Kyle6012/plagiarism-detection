import unittest
from modules.ai_detection import load_ai_detection_model, detect_ai_generated_text

class TestAIDetection(unittest.TestCase):
    def setUp(self):
        self.tokenizer, self.model = load_ai_detection_model()

    def test_ai_detection_score_range(self):
        text = "This is a sample sentence for testing AI detection."
        score = detect_ai_generated_text(text, self.tokenizer, self.model)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

if __name__ == "__main__":
    unittest.main()
