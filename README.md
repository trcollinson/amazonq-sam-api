# AWS SAM REST API

A serverless REST API built with AWS SAM and secured with Amazon Cognito authentication.

## Project Structure

```
.
├── src/                    # Lambda function code
│   ├── hello_world/         # Hello World Lambda function
│   │   ├── app.py           # Lambda handler
│   │   └── requirements.txt  # Function dependencies
│   ├── users/              # Users Lambda function
│   │   ├── app.py           # Lambda handler
│   │   └── requirements.txt  # Function dependencies
│   └── shared/             # Shared code between functions
├── tests/                  # Unit tests
│   ├── test_hello_world.py # Tests for hello_world Lambda
│   └── test_users.py       # Tests for users Lambda
├── template.yaml           # SAM template with Cognito resources
├── pytest.ini             # Pytest configuration
├── requirements-dev.txt    # Development dependencies
└── Makefile               # Commands for testing and deployment
```

## Deployment Instructions

### Prerequisites
- AWS CLI
- AWS SAM CLI
- Python 3.11

### Local Development

To run the API locally:

```bash
sam build
sam local start-api
```

Then access the endpoints at:
- Hello World: http://localhost:3000/hello
- List Users: http://localhost:3000/users
- Get User: http://localhost:3000/users/{username}

**Note:** When testing locally, the Cognito authentication will not be enforced. In the deployed environment, you will need to include a valid JWT token in the Authorization header.

### Deployment

To deploy to AWS:

```bash
sam build
sam deploy --guided
```

## Authentication

This API uses Amazon Cognito for authentication with two user groups:

1. **Standard Users** (`standard-users` group)
   - Can access endpoints that require basic authentication

2. **Admin Users** (`admin-users` group)
   - Have elevated privileges for admin-only endpoints

### Testing with Authentication

After deployment, you'll need to:

1. Create users in the Cognito User Pool
2. Assign users to either the standard or admin group
3. Obtain JWT tokens for API requests

### Making Authenticated Requests

```bash
# Hello World endpoint
curl -H "Authorization: Bearer YOUR_ID_TOKEN" https://your-api-id.execute-api.region.amazonaws.com/Prod/hello

# List all users
curl -H "Authorization: Bearer YOUR_ID_TOKEN" https://your-api-id.execute-api.region.amazonaws.com/Prod/users

# Get specific user
curl -H "Authorization: Bearer YOUR_ID_TOKEN" https://your-api-id.execute-api.region.amazonaws.com/Prod/users/username
```

## Adding New Endpoints

To add a new endpoint:
1. Create a new directory under `src/` for your Lambda function
2. Add the following files to your function directory:
   - `app.py` with your Lambda handler function
   - `requirements.txt` with any dependencies
   - `__init__.py` to make it a Python package
   - `README.md` to document the function
3. Add the function to the `template.yaml` file with appropriate API event configuration
4. Configure the authorization level (any authenticated user or admin only)
5. Create unit tests in the `tests/` directory
6. Deploy the updated application

## Testing

### Setup

Install all project dependencies (both development and all Lambda function dependencies):

```bash
# Install all dependencies
make setup
```

This will install the development dependencies and scan all Lambda function directories for requirements.txt files.

Or install only development dependencies:

```bash
# Install only dev dependencies
make dev-setup

# Or manually
pip install -r requirements-dev.txt
```

### Running Tests

Run tests using the Makefile:

```bash
# Run all tests
make test

# Run tests with coverage report
make test-cov

# Open the coverage report in a browser
make open-cov
```

The coverage report will be generated in HTML format in the `htmlcov/` directory and can be opened automatically with the `open-cov` command.

### Cleaning Up

Remove test artifacts:

```bash
make clean
```