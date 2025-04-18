from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, Fargate, Lambda
from diagrams.aws.database import Aurora, ElasticacheForRedis, Dynamodb
from diagrams.aws.network import CloudFront, Route53, APIGateway
from diagrams.aws.security import WAF, Shield, Cognito, IdentityAndAccessManagementIam, KeyManagementService
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge, SQS
from diagrams.aws.analytics import Kinesis, EMR, Athena, Quicksight
from diagrams.aws.management import Cloudwatch, AutoScaling
from diagrams.aws.general import Users

with Diagram("Enterprise Carbon Footprint Calculator Architecture", show=True, direction="TB"):
    
    # Users
    users = Users("End Users")
    
    with Cluster("Presentation Tier"):
        dns = Route53("DNS")
        cdn = CloudFront("CDN")
        web_protection = WAF("WAF")
        ddos_protection = Shield("DDoS Protection")
        
        frontend_storage = S3("Web/Mobile Assets")
        
    with Cluster("Application Tier"):
        with Cluster("API Layer"):
            api = APIGateway("API Gateway")
            auth = Cognito("Authentication")
        
        with Cluster("Compute Layer"):
            with Cluster("Container Services - Multiple AZs"):
                ecs_cluster = ECS("ECS Cluster")
                fargate_service = Fargate("Fargate Tasks")
                auto_scaling = AutoScaling("Auto Scaling")
        
        with Cluster("Asynchronous Processing"):
            events = Eventbridge("Event Bus")
            queue = SQS("Message Queue")
            serverless = Lambda("Processing Functions")
    
    with Cluster("Data Tier"):
        with Cluster("Operational Data"):
            db = Aurora("Aurora PostgreSQL")
            cache = ElasticacheForRedis("Redis Cache")
            realtime_db = Dynamodb("Real-time Metrics")
        
        with Cluster("Analytics Pipeline"):
            data_stream = Kinesis("Data Streams")
            data_processing = EMR("Data Processing")
            data_query = Athena("Data Querying")
            visualization = Quicksight("Dashboards")
    
    # Security & Monitoring
    iam = IdentityAndAccessManagementIam("IAM")
    encryption = KeyManagementService("KMS")
    monitoring = Cloudwatch("Monitoring & Logs")
    
    # Connections - Presentation Tier
    users >> dns >> cdn
    cdn >> web_protection
    cdn >> ddos_protection
    cdn >> frontend_storage
    cdn >> api
    
    # Connections - Application Tier
    api >> auth
    api >> ecs_cluster
    
    ecs_cluster >> fargate_service
    auto_scaling >> fargate_service
    
    fargate_service >> events
    events >> queue
    queue >> serverless
    
    # Connections - Data Tier
    fargate_service >> db
    fargate_service >> cache
    fargate_service >> realtime_db
    serverless >> db
    serverless >> realtime_db
    
    # Analytics flow
    fargate_service >> data_stream
    data_stream >> data_processing
    data_processing >> data_query
    data_query >> visualization
    
    # Security & Monitoring connections
    encryption >> db
    encryption >> realtime_db
    monitoring >> fargate_service
    monitoring >> serverless
    monitoring >> db
    iam >> fargate_service
    iam >> serverless
    iam >> api