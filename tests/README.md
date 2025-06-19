# Tests

## Purpose
Contains unit tests for the Lambda functions and other components of the SAM REST API.

## Contents
- `test_hello_world.py`: Tests for the hello_world Lambda handler, covering different authentication scenarios
- `test_users.py`: Tests for the users Lambda handler, covering listing users and getting user details
- `__init__.py`: Makes the tests directory a proper Python package

## Testing Approach
Tests follow the unittest framework pattern and test the Lambda handlers with different event types:

```python
def test_lambda_handler_no_auth(self):
    # Test with no authentication
    event = {}
    context = {}
    response = lambda_handler(event, context)
    # Assert expected response
    
def test_lambda_handler_standard_user(self):
    # Test with standard user authentication
    event = {'requestContext': {'authorizer': {'claims': {...}}}}
    # Assert expected response
    
def test_lambda_handler_admin_user(self):
    # Test with admin user authentication
    # Assert expected response
```

## Running Tests
See the main README.md for instructions on running tests using the Makefile commands:
- `make test`: Run all tests
- `make test-cov`: Run tests with coverage report
- `make open-cov`: Open the coverage report in a browser