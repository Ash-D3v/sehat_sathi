import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.disease_identifier import DiseaseIdentifier

class TestDiseaseModel(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.identifier = DiseaseIdentifier()
        except Exception as e:
            self.skipTest(f"Model loading failed: {e}")
    
    def test_disease_prediction(self):
        """Test disease prediction from symptoms"""
        symptoms = ["headache", "fever", "fatigue"]
        result = self.identifier.predict_disease(symptoms)
        
        self.assertIsInstance(result, dict)
        self.assertIn('disease', result)
        self.assertIn('confidence', result)
        self.assertIn('severity', result)
        self.assertIn('recommendations', result)
    
    def test_severity_assessment(self):
        """Test severity assessment"""
        # High severity
        high_severity = self.identifier.assess_severity("heart attack")
        self.assertEqual(high_severity, "high")
        
        # Medium severity
        medium_severity = self.identifier.assess_severity("diabetes")
        self.assertEqual(medium_severity, "medium")
        
        # Low severity
        low_severity = self.identifier.assess_severity("common cold")
        self.assertEqual(low_severity, "low")
    
    def test_recommendations_generation(self):
        """Test recommendations based on disease and severity"""
        recommendations = self.identifier.get_recommendations("fever", "medium")
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        self.assertTrue(all(isinstance(r, str) for r in recommendations))
    
    def test_follow_up_questions(self):
        """Test follow-up questions generation"""
        questions = self.identifier.get_follow_up_questions("diabetes", ["fatigue", "thirst"])
        
        self.assertIsInstance(questions, list)
        self.assertLessEqual(len(questions), 4)  # Should return max 4 questions

if __name__ == '__main__':
    unittest.main()