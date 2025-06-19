import json
import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Lambda function that handles user operations:
    - GET /users: List all users in the Cognito user pool
    - GET /users/{username}: Get information about a specific user
    
    Parameters:
        event (dict): API Gateway Lambda Proxy Input Format
        context (object): Lambda Context runtime methods and attributes
        
    Returns:
        dict: API Gateway Lambda Proxy Output Format
    """
    # Get the user pool ID from environment variables
    user_pool_id = os.environ.get('USER_POOL_ID')
    
    # Check if user is authenticated
    if not event.get('requestContext') or not event['requestContext'].get('authorizer'):
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Unauthorized"
            })
        }
    
    # Create Cognito client
    cognito = boto3.client('cognito-idp')
    
    try:
        # Check if a specific username is provided in the path parameters
        if event.get('pathParameters') and event['pathParameters'].get('username'):
            username = event['pathParameters']['username']
            return get_user(cognito, user_pool_id, username)
        else:
            # List all users
            return list_users(cognito, user_pool_id)
    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "GET,OPTIONS"
            },
            "body": json.dumps({
                "message": f"Error: {str(e)}"
            })
        }

def list_users(cognito, user_pool_id):
    """List all users in the Cognito user pool"""
    response = cognito.list_users(
        UserPoolId=user_pool_id,
        Limit=60
    )
    
    users = []
    for user in response.get('Users', []):
        user_data = {
            'username': user.get('Username'),
            'enabled': user.get('Enabled', False),
            'status': user.get('UserStatus'),
            'created': user.get('UserCreateDate').isoformat() if user.get('UserCreateDate') else None,
            'attributes': {}
        }
        
        # Extract user attributes
        for attr in user.get('Attributes', []):
            user_data['attributes'][attr.get('Name')] = attr.get('Value')
        
        users.append(user_data)
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps({
            "users": users
        })
    }

def get_user(cognito, user_pool_id, username):
    """Get information about a specific user"""
    try:
        # Get user details
        response = cognito.admin_get_user(
            UserPoolId=user_pool_id,
            Username=username
        )
        
        user_data = {
            'username': response.get('Username'),
            'enabled': response.get('Enabled', False),
            'status': response.get('UserStatus'),
            'created': response.get('UserCreateDate').isoformat() if response.get('UserCreateDate') else None,
            'attributes': {},
            'groups': []
        }
        
        # Extract user attributes
        for attr in response.get('UserAttributes', []):
            user_data['attributes'][attr.get('Name')] = attr.get('Value')
            
        # Get user groups
        groups_response = cognito.admin_list_groups_for_user(
            Username=username,
            UserPoolId=user_pool_id
        )
        
        # Add groups to user data
        for group in groups_response.get('Groups', []):
            user_data['groups'].append({
                'name': group.get('GroupName'),
                'description': group.get('Description'),
                'precedence': group.get('Precedence')
            })
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "GET,OPTIONS"
            },
            "body": json.dumps({
                "user": user_data
            })
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                    "Access-Control-Allow-Methods": "GET,OPTIONS"
                },
                "body": json.dumps({
                    "message": f"User {username} not found"
                })
            }
        raise