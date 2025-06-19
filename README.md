# AWS SAM REST API

A serverless REST API built with AWS SAM.

## Project Structure

```
.
├── src/                    # Lambda function code
│   ├── hello_world.py      # Hello World endpoint handler
│   └── requirements.txt    # Python dependencies
└── template.yaml           # SAM template
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
3. Deploy the updated application