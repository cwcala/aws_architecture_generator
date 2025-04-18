# AWS Architecture Diagram Generator

This tool allows you to describe your AWS application architecture in natural language and automatically generates a Python script using the Diagrams package to create a professional AWS architecture diagram.

## How It Works

1. You describe your AWS architecture in natural language
2. The tool calls Amazon Claude 3.7 Sonnet via Amazon Bedrock to interpret your description
3. Claude 3.7 Sonnet generates a Python script using the Diagrams package
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
pip3 install boto3 diagrams
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

You can select the Amazon Bedrock model with `AWS_BEDROCK_MODEL` environment variable and the command below to retreive all Foundation Models your AWS Region provides

```bash
aws bedrock list-foundation-models | jq '.modelSummaries[] | select(.inferenceTypesSupported[] == "ON_DEMAND") | .modelId' 
```

By default : the script will use `anthropic.claude-3-sonnet-20240229-v1:0`

## Usage

1. Run the script:

```bash
python3 aws_architecture_generator.py
```

2. Enter your AWS architecture description when prompted. Type 'done' on a new line when finished.

3. The tool will call Amazon Claude 3.7 Sonnet to generate a Python script based on your description.

4. The generated script will be saved as `generated_aws_diagram_##.py`. The text description of the architecture will be saved as `aws_architecture_description_##.txt`  The ## is a random tracking number assigned to each run.  The input and output tokens are saved as `bedrock_token_usage_xx.log` for each run.

5. You'll be asked if you want to run the script to generate the diagram. If you choose 'y', the diagram will be generated as a PNG file with a title generated from the architecture description.

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
- **ImportError**: You may occasionally get ImportErrors when you try to run the "generated_aws_diagram_xx.py" due to either improper import of modules and submodules for example 'from diagrams.aws.network import CloudFront, Route53, APIGateway, WAF' ImportError: cannot import name 'WAF' from 'diagrams.aws.network' (because WAF must be imported 'from diagrams.aws.security import WAF'.  Note also that services like CloudWatch must be imported as 'from diagrams.aws.network impport Cloudwatch' and DynamoDB must be imported as 'from diagrams.aws.database import Dynamodb' whereas DocumentDB must be imported as 'from diagrams.aws.database import DocumentDB' respecting the EXACT type case described in the Diagrams library. See [Diagrams AWS Nodes reference](https://diagrams.mingrammer.com/docs/nodes/aws) for correct module and submodule import paths and type case. The exact import paths and type cases have also been described in the prompt in the 'aws_architecture_generator.py' file 
- **Diagram Generation Error**: Make sure the diagrams package is properly installed. You may need to install Graphviz as well:
  - On macOS: `brew install graphviz`
  - On Ubuntu/Debian: `apt-get install graphviz`
  - On Windows: Download and install from [Graphviz website](https://graphviz.org/download/)

## Notes

- The quality of the generated diagram depends on the clarity and detail of your description.
- You may need to edit the generated Python script for fine-tuning or to add specific details.
- This tool requires access to Amazon Bedrock and Claude 3.7 Sonnet, which may incur costs according to AWS pricing.
