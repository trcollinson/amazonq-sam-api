# Source Code

## Purpose
Contains all Lambda function handlers and supporting code for the SAM REST API.

## Contents
- `hello_world.py`: Handles the /hello endpoint requests, returning a greeting to authenticated users
- `users.py`: Handles the /users endpoints for listing users and getting user details
- `requirements.txt`: Python dependencies required by the Lambda functions

## Usage
The Lambda handlers follow the standard AWS Lambda handler pattern with API Gateway integration:

```python
def lambda_handler(event, context):
    # Process the API Gateway event
    # Extract user information from Cognito claims if available
    return {
        "statusCode": 200,
        "headers": {...},
        "body": json.dumps({...})
    }
```

## Dependencies
- boto3: AWS SDK for Python, used to interact with Cognito User Pool
- botocore: Core functionality of boto3