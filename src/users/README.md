# Users Lambda

## Purpose
This Lambda function handles user operations for the API:
- GET /users: List all users in the Cognito user pool
- GET /users/{username}: Get information about a specific user

## Contents
- `app.py`: Contains the Lambda handler function and helper functions
- `requirements.txt`: Python dependencies required by this function
- `__init__.py`: Makes the directory a Python package

## Usage
The Lambda handler follows the standard AWS Lambda handler pattern with API Gateway integration:

```python
def lambda_handler(event, context):
    # Check if user is authenticated
    # Determine which operation to perform based on path parameters
    # Return appropriate response
    return {
        "statusCode": 200,
        "headers": {...},
        "body": json.dumps({
            "users": [...] or "user": {...}
        })
    }
```

## Dependencies
- boto3: AWS SDK for Python, used to interact with Cognito User Pool
- botocore: Core functionality of boto3