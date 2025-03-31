from diagrams import Cluster, Diagram
from diagrams.aws.network import Route53, CloudFront, APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Sagemaker, Bedrock
from diagrams.aws.database import Dynamodb
from diagrams.aws.management import Cloudwatch

with Diagram("AWS Application Architecture Diagram Generator", show=False, outformat="png"):
    network_layer = Cluster("Network Layer")
    application_layer = Cluster("Application Layer")
    data_layer = Cluster("Data Layer")
    monitoring_layer = Cluster("Monitoring Layer")

    with network_layer:
        route53 = Route53("Route 53")
        cloudfront = CloudFront("CloudFront")

    with application_layer:
        s3_frontend = S3("S3 (Frontend)")
        api_gateway = APIGateway("API Gateway")
        lambda_request_processor = Lambda("Lambda (Request Processor)")
        bedrock = Bedrock("Bedrock")
        sagemaker_claude = Sagemaker("SageMaker (Claude 3 Sonnet)")
        lambda_execution = Lambda("Lambda (Execution Environment)")

    with data_layer:
        s3_output = S3("S3 (Output Bucket)")
        dynamodb = Dynamodb("DynamoDB")

    with monitoring_layer:
        cloudwatch = Cloudwatch("CloudWatch")

    route53 >> cloudfront >> s3_frontend
    s3_frontend >> api_gateway >> lambda_request_processor
    lambda_request_processor >> bedrock
    bedrock >> sagemaker_claude
    sagemaker_claude >> lambda_execution
    lambda_execution >> s3_output
    lambda_request_processor >> dynamodb
    lambda_execution >> dynamodb
    lambda_request_processor >> cloudwatch
    lambda_execution >> cloudwatch