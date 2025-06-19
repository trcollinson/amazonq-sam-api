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

## Test Coverage Guidelines

1. Aim for high test coverage of Lambda handler functions.
2. Test both success and error paths.
3. Test with different types of input events.
4. Verify all response fields that matter for the API contract.