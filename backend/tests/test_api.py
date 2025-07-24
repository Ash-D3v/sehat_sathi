import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_chat_message_endpoint(self):
        """Test chat message endpoint"""
        payload = {
            'message': 'I have a headache',
            'user_id': 'test_user_123'
        }
        
        response = self.client.post(
            '/api/chat/message',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('bot_reply', data)
        self.assertIn('message_type', data)
    
    def test_chat_message_validation(self):
        """Test chat message validation"""
        # Missing message
        payload = {'user_id': 'test_user'}
        response = self.client.post(
            '/api/chat/message',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Missing user_id
        payload = {'message': 'Hello'}
        response = self.client.post(
            '/api/chat/message',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Empty message
        payload = {'message': '', 'user_id': 'test_user'}
        response = self.client.post(
            '/api/chat/message',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_hospital_search_endpoint(self):
        """Test hospital search endpoint"""
        payload = {
            'location': {'lat': 13.0827, 'lng': 80.2707},  # Chennai coordinates
            'severity': 'medium'
        }
        
        response = self.client.post(
            '/api/health/hospitals/nearby',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('hospitals', data)
        self.assertIn('total_found', data)
    
    def test_emergency_contacts_endpoint(self):
        """Test emergency contacts endpoint"""
        response = self.client.get('/api/health/emergency-contacts/chennai')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('emergency_contacts', data)
        self.assertIn('national_emergency', data)
    
    def test_user_profile_endpoints(self):
        """Test user profile endpoints"""
        user_id = 'test_user_123'
        
        # Get profile (should work even if empty)
        response = self.client.get(f'/api/health/user/{user_id}/profile')
        self.assertEqual(response.status_code, 200)
        
        # Update profile
        profile_data = {
            'name': 'Test User',
            'age': 30,
            'email': 'test@example.com'
        }
        
        response = self.client.post(
            f'/api/health/user/{user_id}/profile',
            data=json.dumps(profile_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_health_tips_endpoint(self):
        """Test health tips endpoint"""
        response = self.client.get('/api/health/health-tips')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('tips', data)
        self.assertIn('language', data)
        
        # Test with language parameter
        response = self.client.get('/api/health/health-tips?language=hindi')
        self.assertEqual(response.status_code, 200)
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/api/nonexistent-endpoint')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()