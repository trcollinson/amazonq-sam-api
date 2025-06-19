import json
import os

def lambda_handler(event, context):
    """
    Lambda function that returns a hello world message for authenticated users.
    
    Parameters:
        event (dict): API Gateway Lambda Proxy Input Format
        context (object): Lambda Context runtime methods and attributes
        
    Returns:
        dict: API Gateway Lambda Proxy Output Format
    """
    # Extract user information from the Cognito authorizer context
    user_info = {}
    if event.get('requestContext') and event['requestContext'].get('authorizer'):
        claims = event['requestContext']['authorizer'].get('claims', {})
        user_info = {
            'email': claims.get('email', 'Unknown'),
            'sub': claims.get('sub', 'Unknown'),
            'cognito:groups': claims.get('cognito:groups', [])
        }
    
    # Check if user is an admin (for future use)
    is_admin = False
    if user_info.get('cognito:groups'):
        if isinstance(user_info['cognito:groups'], str):
            is_admin = 'admin-users' in user_info['cognito:groups']
        else:
            is_admin = 'admin-users' in user_info['cognito:groups']
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps({
            "message": "Hello World!",
            "authenticated": True,
            "user": user_info.get('email'),
            "isAdmin": is_admin
        })
    }