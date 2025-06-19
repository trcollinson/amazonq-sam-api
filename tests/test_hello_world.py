import json
import unittest
import sys
import os

# Add src directory to path so we can import the Lambda function
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from hello_world import lambda_handler

class TestHelloWorld(unittest.TestCase):
    def test_lambda_handler(self):
        # Mock API Gateway event
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

if __name__ == '__main__':
    unittest.main()