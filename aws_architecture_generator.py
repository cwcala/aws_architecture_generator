import boto3
import json
import os
import sys
from pathlib import Path

# Get region and model from environment variables with defaults
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
AWS_BEDROCK_MODEL = os.environ.get('AWS_BEDROCK_MODEL', 'anthropic.claude-3-sonnet-20240229-v1:0')

def get_user_description():
    """Get user's natural language description of their AWS architecture"""
    print("Please describe your AWS application architecture in natural language.")
    print("Include details about components, connections, and any specific requirements.")
    print("Type 'done' on a new line when finished.\n")
    
    lines = []
    while True:
        line = input()
        if line.lower() == 'done':
            break
        lines.append(line)
    
    return "\n".join(lines)

def invoke_bedrock_model(description):
    """Call Amazon Bedrock with the user's description"""
    try:
        # Initialize Bedrock runtime client
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=AWS_DEFAULT_REGION  # Adjust region if needed
        )
        
        # Use Claude 3 Sonnet model　or some other model
        model_id = AWS_BEDROCK_MODEL
        
        # Prepare the prompt for Claude
        prompt = f"""
        I need to create an AWS architecture diagram using the Python Diagrams package.
        
        Here is a description of the architecture:
        
        {description}
        
        Please generate a complete Python script that uses the Diagrams package to create this architecture diagram.
        The script should:
        1. Import all necessary components from the Diagrams package 
        here are some examples of how component imports are done, be careful to use Dynamodb rather than DynamoDBm to import Cloudwatch rather than CloudWatch, Sagemaker rather than SageMaker, and be sure to import APIGateway from the network package:
        from diagrams.aws import *
        from diagrams import *
        from diagrams import Cluster, Diagram
        from diagrams.aws.network import Route53, CloudFront, APIGateway
        from diagrams.aws.storage import S3
        from diagrams.aws.compute import Lambda
        from diagrams.aws.ml import Sagemaker, Bedrock
        from diagrams.aws.database import Dynamodb
        from diagrams.aws.management import Cloudwatch

        2. Create appropriate clusters for different layers (e.g., Network Layer, Application Layer, Data Layer)
        3. Add all relevant AWS services based on the description
        4. Define connections between services and use () around nodes separated by dashes -
        5. Include proper configuration for the diagram (direction, filename, etc.)
        6. Cluster object cannot have link each other
        7. Use '-' operator only if you have an explicit demand
        8. Check and remove double links except when you have an explicit demand
             
        The output should be a complete, runnable Python script that generates a clear and professional AWS architecture diagram.
        """
        
        # Prepare the request body for Claude 3 Sonnet
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        print("\nSending request to Amazon Bedrock (Claude 3 Sonnet)...")
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        # Parse the response
        response_body = json.loads(response.get('body').read())
        
        # Claude 3 Sonnet response format
        if 'content' in response_body and len(response_body.get('content', [])) > 0:
            content_parts = []
            for item in response_body.get('content', []):
                if item.get('type') == 'text':
                    content_parts.append(item.get('text', ''))
            generated_text = '\n'.join(content_parts)
        elif 'completion' in response_body:
            # Claude v2 format (fallback)
            generated_text = response_body.get('completion')
        else:
            # Fallback - try to get any text content
            print("Warning: Unexpected response format. Attempting to extract content...")
            generated_text = str(response_body)
        
        # Extract token usage information
        input_tokens = response_body.get('usage', {}).get('input_tokens', 0)
        output_tokens = response_body.get('usage', {}).get('output_tokens', 0)
        total_tokens = input_tokens + output_tokens
        
        # Log token usage
        print(f"\n=== Token Usage ===")
        print(f"Input Tokens: {input_tokens}")
        print(f"Output Tokens: {output_tokens}")
        print(f"Total Tokens: {total_tokens}")
        
        # Optional: Save token usage to a log file
        with open('bedrock_token_usage.log', 'a') as log_file:
            import datetime
            log_file.write(f"{datetime.datetime.now()}: Input Tokens: {input_tokens}, Output Tokens: {output_tokens}, Total Tokens: {total_tokens}\n")
        
        return generated_text
        
    except Exception as e:
        print(f"Error calling Amazon Bedrock: {str(e)}")
        return None

def extract_python_code(text):
    """Extract Python code from the Bedrock model response"""
    # Look for code blocks in markdown format
    if "```python" in text and "```" in text:
        # Extract code between ```python and ```
        start_idx = text.find("```python") + len("```python")
        end_idx = text.find("```", start_idx)
        code = text[start_idx:end_idx].strip()
        return code
    
    # If no markdown code blocks, try to extract based on imports
    elif "from diagrams import" in text:
        # Find the start of the Python code
        start_idx = text.find("from diagrams import")
        # Extract everything from that point
        code = text[start_idx:].strip()
        return code
    
    # Return the full text if we can't identify code blocks
    return text

def save_diagram_script(code):
    """Save the generated Python script to a file"""
    script_path = "generated_aws_diagram.py"
    
    with open(script_path, "w") as f:
        f.write(code)
    
    print(f"\nDiagram script saved to: {script_path}")
    return script_path

def run_diagram_script(script_path):
    """Run the generated diagram script"""
    try:
        print("\nGenerating diagram...")
        # Try python3 first, fall back to python if needed
        result = os.system(f"python3 {script_path}")
        if result != 0:
            print("Trying with 'python' command...")
            os.system(f"python {script_path}")
        print("\nDiagram generation complete!")
        
        # Look for generated PNG files
        diagram_files = list(Path('.').glob('*.png'))
        if diagram_files:
            print(f"\nGenerated diagram file: {diagram_files[0]}")
        
    except Exception as e:
        print(f"Error generating diagram: {str(e)}")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        # Check boto3
        import boto3
        print("✓ boto3 is installed")
    except ImportError:
        print("✗ boto3 is not installed. Please install it using: pip install boto3")
        return False
    
    try:
        # Check diagrams
        import diagrams
        print("✓ diagrams is installed")
    except ImportError:
        print("✗ diagrams is not installed. Please install it using: pip install diagrams")
        return False
    
    try:
        # Check if graphviz is installed by running a simple command
        import subprocess
        result = subprocess.run(['dot', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("✓ graphviz is installed")
        else:
            print("✗ graphviz may not be installed or not in PATH")
            print("  Please install graphviz:")
            print("  - macOS: brew install graphviz")
            print("  - Ubuntu/Debian: apt-get install graphviz")
            print("  - Windows: Download from https://graphviz.org/download/")
            return False
    except Exception:
        print("✗ Could not verify graphviz installation")
        print("  Please ensure graphviz is installed:")
        print("  - macOS: brew install graphviz")
        print("  - Ubuntu/Debian: apt-get install graphviz")
        print("  - Windows: Download from https://graphviz.org/download/")
        print("\nContinuing anyway, but diagram generation may fail...")
    
    return True

def main():
    try:
        print("\n=== AWS Architecture Diagram Generator ===\n")
        
        # Check dependencies
        print("Checking dependencies...")
        check_dependencies()
        print()
        
        # Step 1: Get user's description
        description = get_user_description()
        if not description:
            print("No description provided. Exiting.")
            return
        
        # Step 2: Call Bedrock model
        generated_text = invoke_bedrock_model(description)
        if not generated_text:
            print("Failed to generate diagram code. Exiting.")
            return
        
        # Step 3: Extract Python code
        python_code = extract_python_code(generated_text)
        
        # Step 4: Save the user's description
        description_path = "aws_architecture_description.txt"
        with open(description_path, "w") as f:
            f.write(description)
        print(f"\nYour architecture description saved to: {description_path}")
        
        # Step 5: Save the script
        script_path = save_diagram_script(python_code)
        
        # Step 6: Ask if user wants to run the script
        run_script = input("\nWould you like to run the script to generate the diagram? (y/n): ").lower()
        if run_script == 'y':
            run_diagram_script(script_path)
        
        print("\nDone!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
