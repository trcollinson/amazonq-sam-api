# Testing Strategy for AWS SAM API Project

## General Testing Principles

1. **Test behavior, not implementation**: Focus on testing the expected behavior of functions rather than their internal implementation details.

2. **Resilient assertions**: Use assertions that are resilient to minor implementation changes.

3. **Minimize mocking**: Only mock external dependencies when necessary, not the functions being tested.

## Lambda Function Testing Guidelines

### For API Gateway Lambda Functions:

1. **Test with different event types**:
   - No authentication context
   - Standard user authentication
   - Admin user authentication

2. **Check response structure**:
   - Verify status code
   - Verify headers
   - Parse and verify body content

3. **Avoid brittle assertions**:
   - Use `assertIn('key', dict)` to check for key existence instead of `assertEqual(dict['key'], value)` when the exact value isn't critical
   - Use `assertIsNotNone()` only when you expect a non-None value

4. **Handle authentication data properly**:
   - Mock the Cognito claims structure in test events
   - Test both presence and absence of authentication data

## Example Test Pattern

```python
def test_lambda_handler_no_auth(self):
    # Mock API Gateway event with no auth
    event = {}
    context = {}
    
    # Call the function
    response = lambda_handler(event, context)
    
    # Check the response structure
    self.assertEqual(response['statusCode'], 200)
    self.assertEqual(response['headers']['Content-Type'], 'application/json')
    
    # Parse the body and check content
    body = json.loads(response['body'])
    self.assertEqual(body['message'], 'Hello World!')
    
    # Check for key existence rather than exact value
    self.assertIn('user', body)
    self.assertIn('isAdmin', body)
```

## When to Use Mocking

1. **Mock external AWS services** (S3, DynamoDB, etc.) that the Lambda function interacts with.

2. **Mock environment variables** that the function uses.

3. **Don't mock the function being tested** or its internal methods unless absolutely necessary.

4. **Use patch decorators** to mock dependencies:
   ```python
   @patch('boto3.client')
   def test_with_mock_aws_service(self, mock_boto_client):
       # Configure the mock
       mock_s3 = MagicMock()
       mock_boto_client.return_value = mock_s3
       
       # Test the function
       # ...
   ```

5. **Mock complex objects with expected methods**:
   When mocking responses that contain objects with methods that your code calls, use MagicMock with appropriate method implementations:
   ```python
   # Instead of using a string for a date that needs isoformat() called on it:
   'UserCreateDate': '2023-01-01 12:00:00',  # WRONG - will cause AttributeError
   
   # Use a MagicMock with the expected method:
   'UserCreateDate': MagicMock(isoformat=lambda: '2023-01-01T12:00:00Z'),  # CORRECT
   ```

## Test Coverage Guidelines

1. Aim for high test coverage of Lambda handler functions.
2. Test both success and error paths.
3. Test with different types of input events.
4. Verify all response fields that matter for the API contract.

## Common Testing Pitfalls

1. **Missing imports in test files**: Always ensure all necessary modules are imported in test files, especially when mocking external services.

2. **Type mismatches in mock responses**: Ensure mock responses match the expected types that the function will process. Pay special attention to:
   - Date objects that need methods like `isoformat()`
   - Nested structures that might be accessed with dot notation
   - Objects with methods that are called in the code being tested

3. **Incomplete mock configuration**: When mocking AWS services, ensure all methods used by your code are properly configured on the mock object.

4. **Mocking AWS exceptions correctly**: When mocking AWS service exceptions, use the actual exception classes from botocore:
   ```python
   # WRONG - MagicMock is not an exception class:
   mock_exception = MagicMock()
   mock_exception.response = {'Error': {'Code': 'ErrorCode'}}
   mock_client.method.side_effect = mock_exception  # TypeError: catching classes that do not inherit from BaseException is not allowed
   
   # WRONG - Custom exception without proper structure:
   class MockClientError(Exception):
       pass
   error = MockClientError()
   error.response = {'Error': {'Code': 'ErrorCode'}}
   mock_client.method.side_effect = error  # May work for simple cases but doesn't fully mimic AWS exceptions
   
   # CORRECT - Import and use the actual ClientError exception:
   from botocore.exceptions import ClientError
   
   error_response = {'Error': {'Code': 'UserNotFoundException', 'Message': 'User does not exist'}}
   mock_client.method.side_effect = ClientError(error_response=error_response, operation_name='OperationName')
   ```

5. **JSON serialization issues**: When mocking objects that will be serialized to JSON, ensure they are JSON-serializable:
   ```python
   # WRONG - MagicMock objects are not JSON serializable:
   response = {
       'data': MagicMock(),  # Will cause TypeError: Object of type MagicMock is not JSON serializable
   }
   
   # CORRECT - Use simple Python types that are JSON serializable:
   response = {
       'data': {
           'id': '123',
           'name': 'test',
           'attributes': ['a', 'b', 'c']
       }
   }
   ```