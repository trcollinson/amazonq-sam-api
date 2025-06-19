# AWS SAM REST API

A serverless REST API built with AWS SAM and secured with Amazon Cognito authentication.

## Project Structure

```
.
├── src/                    # Lambda function code
│   ├── hello_world.py      # Hello World endpoint handler
│   └── requirements.txt    # Python dependencies
├── tests/                  # Unit tests
│   └── test_hello_world.py # Tests for hello_world Lambda
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

Then access the hello endpoint at: http://localhost:3000/hello

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
curl -H "Authorization: Bearer YOUR_ID_TOKEN" https://your-api-id.execute-api.region.amazonaws.com/Prod/hello
```

## Adding New Endpoints

To add a new endpoint:
1. Create a new handler function in the `src/` directory
2. Add the function to the `template.yaml` file with appropriate API event configuration
3. Configure the authorization level (any authenticated user or admin only)
4. Create unit tests in the `tests/` directory
5. Deploy the updated application

## Testing

### Setup

Install development dependencies:

```bash
# Using make command
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