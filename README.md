# AWS Architecture Diagram Generator

This tool allows you to describe your AWS application architecture in natural language and automatically generates a Python script using the Diagrams package to create a professional AWS architecture diagram.

## How It Works

1. You describe your AWS architecture in natural language
2. The tool calls Amazon Claude 3 Sonnet via Amazon Bedrock to interpret your description
3. Claude 3 Sonnet generates a Python script using the Diagrams package
4. The script is saved to a file and can be executed to create the diagram

## Prerequisites

- Python 3.6+
- AWS account with access to Amazon Bedrock and Claude 3 Sonnet
- AWS credentials configured
- Required Python packages:
  - boto3
  - diagrams

## Installation

1. Install the required Python packages:

```bash
pip install boto3 diagrams
```

2. Make sure you have AWS credentials configured with access to Amazon Bedrock. You can configure credentials using:

```bash
aws configure
```

Or by setting environment variables:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## Usage

1. Run the script:

```bash
python aws_architecture_generator.py
```

2. Enter your AWS architecture description when prompted. Type 'done' on a new line when finished.

3. The tool will call Amazon Claude 3 Sonnet to generate a Python script based on your description.

4. The generated script will be saved as `generated_aws_diagram.py`.

5. You'll be asked if you want to run the script to generate the diagram. If you choose 'y', the diagram will be generated as a PNG file.

## Example

Here's an example of a natural language description you might provide:

```
I need a 3-tier web application architecture on AWS. 
It should have a frontend hosted on S3 and distributed via CloudFront.
The middle tier should use API Gateway and Lambda functions.
For the database tier, I want to use DynamoDB for the main data store and S3 for file storage.
Users should authenticate using Cognito.
The Lambda functions should be able to access both DynamoDB and S3.
done
```

## Troubleshooting

- **AWS Credentials Error**: Make sure your AWS credentials are properly configured and have access to Amazon Bedrock.
- **Region Error**: Ensure you're using a region where Amazon Bedrock and Claude 3 Sonnet are available (e.g., us-east-1).
- **Python Command Error**: If you see an error about the `python` command not being found, the script will automatically try to use `python3` instead. If both fail, ensure Python is installed and in your PATH.
- **Diagram Generation Error**: Make sure the diagrams package is properly installed. You may need to install Graphviz as well:
  - On macOS: `brew install graphviz`
  - On Ubuntu/Debian: `apt-get install graphviz`
  - On Windows: Download and install from [Graphviz website](https://graphviz.org/download/)

## Notes

- The quality of the generated diagram depends on the clarity and detail of your description.
- You may need to edit the generated Python script for fine-tuning or to add specific details.
- This tool requires access to Amazon Bedrock and Claude 3 Sonnet, which may incur costs according to AWS pricing.
