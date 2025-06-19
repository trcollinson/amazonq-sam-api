import json
import unittest
import sys
import os
import boto3
from botocore.exceptions import ClientError
from unittest.mock import patch, MagicMock

# Add src directory to path so we can import the Lambda function
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from users import lambda_handler

class TestUsers(unittest.TestCase):
    @patch('users.boto3.client')
    def test_list_users_standard_user(self, mock_boto_client):
        # Set up mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Mock the list_users response
        mock_cognito.list_users.return_value = {
            'Users': [
                {
                    'Username': 'user1',
                    'Enabled': True,
                    'UserStatus': 'CONFIRMED',
                    'UserCreateDate': MagicMock(isoformat=lambda: '2023-01-01T12:00:00Z'),
                    'Attributes': [
                        {'Name': 'email', 'Value': 'user1@example.com'},
                        {'Name': 'custom:role', 'Value': 'standard'}
                    ]
                },
                {
                    'Username': 'user2',
                    'Enabled': True,
                    'UserStatus': 'CONFIRMED',
                    'UserCreateDate': MagicMock(isoformat=lambda: '2023-01-02T12:00:00Z'),
                    'Attributes': [
                        {'Name': 'email', 'Value': 'user2@example.com'},
                        {'Name': 'custom:role', 'Value': 'admin'}
                    ]
                }
            ]
        }
        
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
        
        # Set environment variables
        os.environ['USER_POOL_ID'] = 'us-east-1_example'
        
        # Call the function
        response = lambda_handler(event, context)
        
        # Check the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        
        # Parse the body and check the users
        body = json.loads(response['body'])
        self.assertIn('users', body)
        self.assertEqual(len(body['users']), 2)
        self.assertEqual(body['users'][0]['username'], 'user1')
        self.assertEqual(body['users'][1]['username'], 'user2')
        
        # Verify the mock was called with the correct arguments
        mock_cognito.list_users.assert_called_once_with(
            UserPoolId='us-east-1_example',
            Limit=60
        )
    
    @patch('users.boto3.client')
    def test_get_user_standard_user(self, mock_boto_client):
        # Set up mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Mock the admin_get_user response
        mock_cognito.admin_get_user.return_value = {
            'Username': 'user1',
            'Enabled': True,
            'UserStatus': 'CONFIRMED',
            'UserCreateDate': MagicMock(isoformat=lambda: '2023-01-01T12:00:00Z'),
            'UserAttributes': [
                {'Name': 'email', 'Value': 'user1@example.com'},
                {'Name': 'custom:role', 'Value': 'standard'}
            ]
        }
        
        # Mock the admin_list_groups_for_user response
        mock_cognito.admin_list_groups_for_user.return_value = {
            'Groups': [
                {
                    'GroupName': 'standard-users',
                    'Description': 'Standard users with basic access',
                    'Precedence': 10
                }
            ]
        }
        
        # Mock API Gateway event with standard user auth and path parameters
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'email': 'user@example.com',
                        'sub': '12345',
                        'cognito:groups': 'standard-users'
                    }
                }
            },
            'pathParameters': {
                'username': 'user1'
            }
        }
        context = {}
        
        # Set environment variables
        os.environ['USER_POOL_ID'] = 'us-east-1_example'
        
        # Call the function
        response = lambda_handler(event, context)
        
        # Check the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        
        # Parse the body and check the user
        body = json.loads(response['body'])
        self.assertIn('user', body)
        self.assertEqual(body['user']['username'], 'user1')
        self.assertEqual(body['user']['attributes']['email'], 'user1@example.com')
        
        # Check groups
        self.assertIn('groups', body['user'])
        self.assertEqual(len(body['user']['groups']), 1)
        self.assertEqual(body['user']['groups'][0]['name'], 'standard-users')
        
        # Verify the mocks were called with the correct arguments
        mock_cognito.admin_get_user.assert_called_once_with(
            UserPoolId='us-east-1_example',
            Username='user1'
        )
        mock_cognito.admin_list_groups_for_user.assert_called_once_with(
            UserPoolId='us-east-1_example',
            Username='user1'
        )
    
    @patch('users.boto3.client')
    def test_get_user_not_found(self, mock_boto_client):
        # Set up mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Create a proper ClientError exception
        error_response = {
            'Error': {
                'Code': 'UserNotFoundException',
                'Message': 'User does not exist'
            }
        }
        
        # Use the actual ClientError exception
        mock_cognito.admin_get_user.side_effect = ClientError(
            error_response=error_response,
            operation_name='AdminGetUser'
        )
        
        # Mock API Gateway event with standard user auth and path parameters
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'email': 'user@example.com',
                        'sub': '12345',
                        'cognito:groups': 'standard-users'
                    }
                }
            },
            'pathParameters': {
                'username': 'nonexistent'
            }
        }
        context = {}
        
        # Set environment variables
        os.environ['USER_POOL_ID'] = 'us-east-1_example'
        
        # Call the function
        response = lambda_handler(event, context)
        
        # Check the response
        self.assertEqual(response['statusCode'], 404)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        
        # Parse the body and check the message
        body = json.loads(response['body'])
        self.assertIn('message', body)
        self.assertIn('not found', body['message'])
        
        # Verify the mock was called with the correct arguments
        mock_cognito.admin_get_user.assert_called_once_with(
            UserPoolId='us-east-1_example',
            Username='nonexistent'
        )
    
    def test_unauthorized_access(self):
        # Mock API Gateway event with no auth
        event = {}
        context = {}
        
        # Call the function
        response = lambda_handler(event, context)
        
        # Check the response
        self.assertEqual(response['statusCode'], 401)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        
        # Parse the body and check the message
        body = json.loads(response['body'])
        self.assertIn('message', body)
        self.assertEqual(body['message'], 'Unauthorized')

if __name__ == '__main__':
    unittest.main()