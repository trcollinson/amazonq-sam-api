# Shared Code

## Purpose
This directory contains shared code that can be used across multiple Lambda functions.

## Usage
To use shared code in a Lambda function, you need to:

1. Include the shared code in the Lambda function's deployment package
2. Import the shared modules in your Lambda function code

Example:
```python
from shared.utils import some_utility_function

def lambda_handler(event, context):
    result = some_utility_function()
    # ...
```