# AWS SAM REST API

A serverless REST API built with AWS SAM.

## Project Structure

```
.
├── src/                    # Lambda function code
│   ├── hello_world.py      # Hello World endpoint handler
│   └── requirements.txt    # Python dependencies
├── tests/                  # Unit tests
│   └── test_hello_world.py # Tests for hello_world Lambda
├── template.yaml           # SAM template
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

### Deployment

To deploy to AWS:

```bash
sam build
sam deploy --guided
```

## Adding New Endpoints

To add a new endpoint:
1. Create a new handler function in the `src/` directory
2. Add the function to the `template.yaml` file with appropriate API event configuration
3. Create unit tests in the `tests/` directory
4. Deploy the updated application

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