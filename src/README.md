# Source Code

## Purpose
Contains all Lambda function handlers and supporting code for the SAM REST API.

## Contents
- `hello_world.py`: Handles the /hello endpoint requests, returning a greeting to authenticated users
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
- No external dependencies currently required beyond the AWS Lambda runtime