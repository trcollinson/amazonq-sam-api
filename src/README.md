# Source Code

## Purpose
Contains all Lambda function handlers and supporting code for the SAM REST API.

## Contents
- `hello_world/`: Lambda function for the /hello endpoint
- `users/`: Lambda function for user operations (/users endpoints)
- `shared/`: Common code that can be used across multiple Lambda functions

## Directory Structure
Each Lambda function follows this structure:
```
function_name/
├── __init__.py       # Makes the directory a Python package
├── app.py            # Contains the lambda_handler function
├── requirements.txt  # Function-specific dependencies
└── README.md         # Documentation for the function
```

## Benefits of This Structure
- **Better organization**: Each Lambda function has its own dedicated directory
- **Cleaner dependencies**: Each function can have its own requirements.txt
- **Easier deployment**: SAM can package each function independently
- **Improved maintainability**: Clearer separation of concerns