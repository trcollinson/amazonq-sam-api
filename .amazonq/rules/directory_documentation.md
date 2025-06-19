# Directory-Level Documentation Guidelines

## Purpose
This rule establishes a standard for creating and maintaining directory-level documentation to improve code organization, readability, and generation efficiency.

## Directory Documentation Structure

Each significant directory should contain a `README.md` file with the following sections:

### 1. Directory Purpose
```markdown
# Directory Name

## Purpose
Brief description of what this directory contains and its role in the project.
```

### 2. Content Organization
```markdown
## Contents
- `file1.py`: Description of file's purpose
- `file2.py`: Description of file's purpose
- `subdirectory/`: Description of subdirectory's purpose
```

### 3. Usage Examples
```markdown
## Usage
Brief examples of how the code in this directory is used.
```

### 4. Dependencies
```markdown
## Dependencies
List of external dependencies or other project modules this code depends on.
```

## Implementation Guidelines

1. **Create README.md files** in each significant directory:
   - `/src/`
   - `/tests/`
   - Any feature-specific subdirectories

2. **Update documentation when adding new files** to maintain accuracy.

3. **Include code examples** for complex functionality.

4. **Document interfaces** between different components.

5. **Keep documentation concise** - aim for clarity over verbosity.

## Example Directory Documentation

### For `/src/` Directory:

```markdown
# Source Code

## Purpose
Contains all Lambda function handlers and supporting modules for the API.

## Contents
- `hello_world.py`: Handles the /hello endpoint requests
- `utils/`: Common utility functions used across multiple handlers
- `models/`: Data models and schema definitions

## Usage
Lambda handlers follow the standard AWS Lambda handler pattern:
```python
def lambda_handler(event, context):
    # Process event
    return response
```

## Dependencies
- AWS SDK for Python (boto3)
- JSON Web Token (PyJWT) for token validation
```

### For `/tests/` Directory:

```markdown
# Tests

## Purpose
Contains unit and integration tests for the API.

## Contents
- `test_hello_world.py`: Tests for the hello_world Lambda handler
- `conftest.py`: Pytest fixtures and configuration
- `mocks/`: Mock objects and data for testing

## Running Tests
See the main README.md for instructions on running tests.
```

## Benefits

1. **Improved code generation**: Amazon Q can use this documentation to understand the project structure and generate more appropriate code.

2. **Faster onboarding**: New developers can quickly understand the codebase.

3. **Better maintainability**: Documentation helps maintain consistency as the project evolves.

4. **Reduced duplication**: Clear documentation of existing functionality prevents reimplementation.