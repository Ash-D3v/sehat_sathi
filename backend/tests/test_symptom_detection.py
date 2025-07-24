import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.symptom_detector import SymptomDetector

class TestSymptomDetection(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = SymptomDetector()
    
    def test_english_symptom_detection(self):
        """Test symptom detection in English"""
        test_cases = [
            ("I have a headache and fever", True),
            ("My stomach hurts badly", True),
            ("Hello, how are you?", False),
            ("I feel pain in my chest", True),
            ("What's the weather today?", False)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = self.detector.analyze_input(text)
                self.assertEqual(result['has_symptoms'], expected)
    
    def test_hindi_symptom_detection(self):
        """Test symptom detection in Hindi"""
        test_cases = [
            ("मुझे सिरदर्द और बुखार है", True),
            ("मेरे पेट में दर्द है", True),
            ("नमस्ते, आप कैसे हैं?", False)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = self.detector.analyze_input(text)
                self.assertEqual(result['has_symptoms'], expected)
    
    def test_language_detection(self):
        """Test language detection"""
        test_cases = [
            ("I have a headache", "english"),
            ("मुझे सिरदर्द है", "hindi"),
            ("எனக்கு தலைவலி", "tamil")
        ]
        
        for text, expected_lang in test_cases:
            with self.subTest(text=text):
                detected_lang = self.detector.detect_language(text)
                self.assertEqual(detected_lang, expected_lang)
    
    def test_keyword_detection(self):
        """Test keyword-based detection"""
        # English keywords
        self.assertTrue(
            self.detector.keyword_based_detection("I have pain", "english")
        )
        self.assertFalse(
            self.detector.keyword_based_detection("Nice weather", "english")
        )
        
        # Hindi keywords  
        self.assertTrue(
            self.detector.keyword_based_detection("मुझे दर्द है", "hindi")
        )
    
    def test_follow_up_questions(self):
        """Test follow-up question generation"""
        symptoms = ["headache", "fever"]
        questions = self.detector.get_follow_up_questions(symptoms, "english")
        
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        self.assertTrue(all(isinstance(q, str) for q in questions))

if __name__ == '__main__':
    unittest.main()