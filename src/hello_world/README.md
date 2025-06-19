# Hello World Lambda

## Purpose
This Lambda function handles the `/hello` endpoint, returning a greeting to authenticated users.

## Contents
- `app.py`: Contains the Lambda handler function
- `requirements.txt`: Python dependencies required by this function
- `__init__.py`: Makes the directory a Python package

## Usage
The Lambda handler follows the standard AWS Lambda handler pattern with API Gateway integration:

```python
def lambda_handler(event, context):
    # Extract user information from Cognito claims
    # Return a greeting with user information
    return {
        "statusCode": 200,
        "headers": {...},
        "body": json.dumps({
            "message": "Hello World!",
            "authenticated": True,
            "user": user_email,
            "isAdmin": is_admin
        })
    }
```

## Dependencies
- No external dependencies required