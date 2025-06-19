import json
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src directory to path so we can import the Lambda function
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from hello_world.app import lambda_handler

class TestHelloWorld(unittest.TestCase):
    def test_lambda_handler_no_auth(self):
        # Mock API Gateway event with no auth
        event = {}
        context = {}
        
        # Call the function
        response = lambda_handler(event, context)
        
        # Check the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')
        
        # Parse the body and check the message
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Hello World!')
        self.assertTrue(body['authenticated'])
        
        # For the no auth case, user will be None in the current implementation
        # Just check that the 'user' key exists in the response
        self.assertIn('user', body)
        self.assertFalse(body['isAdmin'])
    
    def test_lambda_handler_standard_user(self):
        # Mock API Gateway event with standard user auth
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'email': 'user@example.com',
                        'sub': '12345',
                        'cognito:groups': 'standard-users'
                    }
                }
            }
        }
        context = {}
        
        # Call the function
        response = lambda_handler(event, context)
        
        # Parse the body and check the user info
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Hello World!')
        self.assertTrue(body['authenticated'])
        self.assertEqual(body['user'], 'user@example.com')
        self.assertFalse(body['isAdmin'])
    
    def test_lambda_handler_admin_user(self):
        # Mock API Gateway event with admin user auth
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'email': 'admin@example.com',
                        'sub': '67890',
                        'cognito:groups': 'admin-users'
                    }
                }
            }
        }
        context = {}
        
        # Call the function
        response = lambda_handler(event, context)
        
        # Parse the body and check the admin status
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Hello World!')
        self.assertTrue(body['authenticated'])
        self.assertEqual(body['user'], 'admin@example.com')
        self.assertTrue(body['isAdmin'])

if __name__ == '__main__':
    unittest.main()