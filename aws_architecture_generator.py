import boto3
import json
import os
import sys
import random
from pathlib import Path
from botocore.exceptions import ClientError
import importlib
import pkgutil
import ast
import re
from diagrams import __path__ as diagrams_path

"""
Anthropic Claude 3.7 Sonnet reasoning capability
with Amazon Bedrock
- Set up Amazon Bedrock runtime client
- Create a message
- Configure reasoning parameters
- Send a request with reasoning enabled
- Process both the reasoning output and final response
"""

# Get region and model from environment variables with defaults
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
AWS_BEDROCK_MODEL = os.environ.get('AWS_BEDROCK_MODEL', 'us.anthropic.claude-3-7-sonnet-20250219-v1:0' ) #'anthropic.claude-3-sonnet-20240229-v1:0'
tracking_number = random.randint(1, 1000)  
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
        # Create and initialize the Amazon Bedrock runtime client
        bedrock_runtime  = boto3.client(service_name="bedrock-runtime",region_name=AWS_DEFAULT_REGION)
        # Specify the model ID. For the latest available models, see:
        # https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
        model_id = AWS_BEDROCK_MODEL #"us.anthropic.claude-3-7-sonnet-20250219-v1:0" or "us.anthropic.claude-3-7-sonnet-20250219-v1:0" #AWS_BEDROCK_MODEL #'amazon.nova-pro-v1:0' 
        
        # Prepare the prompt for Claude
        prompt = f"""
        Acting as a cloud architect, please provide a complete runnable Python script using the diagrams library, adhering strictly to the official documentation at https://diagrams.mingrammer.com/docs/nodes/aws. 
        Use ONLY these exact module and submodule imports in the python code respecting exact diagrams categories, spelling, and type-case including camelcase when importing and calling aws service icons in order to avoid import errors :
        from diagrams.aws.analytics import AmazonOpensearchService, Analytics, Athena,CloudsearchSearchDocuments,Cloudsearch,DataLakeResource,DataPipeline,ElasticsearchService,ES,EMRCluster, EMREngineMaprM3,EMREngineMaprM5,EMREngineMaprM7,EMREngine,EMRHdfsCluster,EMR,GlueCrawlers,GlueDataCatalog,Glue,KinesisDataAnalytics,KinesisDataFirehose,KinesisDataStreams,KinesisVideoStreams,Kinesis,LakeFormation,ManagedStreamingForKafka,Quicksight, RedshiftDenseComputeNode, RedshiftDenseStorageNode, Redshift 
        from diagrams.aws.ar import ArVr, Sumerian
        from diagrams.aws.blockchain import Blockchain, ManagedBlockchain,QuantumLedgerDatabaseQldb, QLDB
        from diagrams.aws.business import AlexaForBusiness, A4B, BusinessApplications,Chime,Workmail
        from diagrams.aws.compute import AppRunner, ApplicationAutoScaling, AutoScaling, Batch,ComputeOptimizer,Compute, EC2Ami, AMI,EC2AutoScaling,EC2ContainerRegistryImage,EC2ContainerRegistryRegistry,EC2ContainerRegistry,ECR,EC2ElasticIpAddress,EC2ImageBuilder, EC2Instance, EC2Instances,EC2Rescue,EC2SpotInstance,EC2,ElasticBeanstalkApplication,ElasticBeanstalkDeployment, ElasticBeanstalk,EB,ElasticContainerServiceContainer, ElasticContainerServiceService,ElasticContainerService,ECS,ElasticKubernetesService,EKS,Fargate, LambdaFunction,Lambda, Lightsail, LocalZones,Outposts,ServerlessApplicationRepository, SAR,ThinkboxDeadline, ThinkboxDraft, ThinkboxFrost,ThinkboxKrakatoa,ThinkboxSequoia,ThinkboxStoke,ThinkboxXmesh, VmwareCloudOnAWS, Wavelength    
        from diagrams.aws.cost import Budgets, CostAndUsageReport,CostExplorer,CostManagement,ReservedInstanceReporting,SavingsPlans 
        from diagrams.aws.database import AuroraInstance, Aurora, DatabaseMigrationServiceDatabaseMigrationWorkflow,DatabaseMigrationService, DMS, Database,DB, DocumentdbMongodbCompatibility, DocumentDB,DynamodbAttribute,DynamodbAttributes,DynamodbDax, DAX,DynamodbGlobalSecondaryIndex,DynamodbGSI,DynamodbItem,DynamodbItems,DynamodbStreams, DynamodbTable,Dynamodb, DDB,ElasticacheCacheNode,ElasticacheForMemcached,ElasticacheForRedis,Elasticache,ElastiCache,KeyspacesManagedApacheCassandraService, Neptune,QuantumLedgerDatabaseQldb, QLDB,RDSInstance, RDSMariadbInstance, RDSMysqlInstance, RDSOnVmware, RDSOracleInstance,RDSPostgresqlInstance, RDSSqlServerInstance, RDS,RedshiftDenseComputeNode,RedshiftDenseStorageNode,Redshift,Timestream                       
        from diagrams.aws.devtools import CloudDevelopmentKit, Cloud9Resource, Cloud9, Codeartifact,Codebuild,Codecommit,Codedeploy,Codepipeline,Codestar,CommandLineInterface, CLI,DeveloperTools, DevTools,ToolsAndSdks, XRay
        from diagrams.aws.enablement import CustomerEnablement, Iq,ManagedServices,ProfessionalServices,Support
        from diagrams.aws.enduser import Appstream20, DesktopAndAppStreaming, Workdocs,Worklink,Workspaces
        from diagrams.aws.engagement import Connect,CustomerEngagement,Pinpoint, SimpleEmailServiceSesEmail,SimpleEmailServiceSes, SES
        from diagrams.aws.games import GameTech, Gamelift
        from diagrams.aws.general import Client, Disk, Forums, General, GenericDatabase, GenericFirewall,GenericOfficeBuilding,OfficeBuilding,GenericSamlToken,GenericSDK,InternetAlt1, InternetAlt2,InternetGateway,Marketplace,MobileClient,Multimedia,OfficeBuilding,SamlToken, SDK, SslPadlock,TapeStorage,Toolkit,TraditionalServer,User, Users                             
        from diagrams.aws.integration import ApplicationIntegration,Appsync,ConsoleMobileApplication,EventResource,EventbridgeCustomEventBusResource,EventbridgeDefaultEventBusResource,EventbridgeSaasPartnerEventBusResource,Eventbridge,ExpressWorkflows,MQ,SimpleNotificationServiceSnsEmailNotification,SimpleNotificationServiceSnsHttpNotification,SimpleNotificationServiceSnsTopic,SimpleNotificationServiceSns, SNS,SimpleQueueServiceSqsMessage,SimpleQueueServiceSqsQueue,SimpleQueueServiceSqs, SQS,StepFunctions, SF 
        from diagrams.aws.iot import Freertos, FreeRTOS,InternetOfThings,Iot1Click,IotAction,IotActuator,IotAlexaEcho,IotAlexaEnabledDevice,IotAlexaSkill,IotAlexaVoiceService,IotAnalyticsChannel,IotAnalyticsDataSet,IotAnalyticsDataStore,IotAnalyticsNotebook,IotAnalyticsPipeline,IotAnalytics,IotBank,IotBicycle,IotButton,IotCamera,IotCar,IotCart,IotCertificate,IotCoffeePot,IotCore,IotDesiredState,IotDeviceDefender,IotDeviceGateway,IotDeviceManagement,IotDoorLock,IotEvents,IotFactory,IotFireTvStick,IotFireTv,IotGeneric,IotGreengrassConnector,IotGreengrass,IotHardwareBoard, IotBoard,IotHouse,IotHttp,IotHttp2,IotJobs,IotLambda,IotLightbulb,IotMedicalEmergency,IotMqtt,IotOverTheAirUpdate,IotPolicyEmergency,IotPolicy,IotReportedState,IotRule,IotSensor,IotServo,IotShadow,IotSimulator,IotSitewise,IotThermostat,IotThingsGraph,IotTopic,IotTravel,IotUtility,IotWindfarm
        from diagrams.aws.management import AmazonDevopsGuru,AmazonManagedGrafana,AmazonManagedPrometheus,AmazonManagedWorkflowsApacheAirflow,AutoScaling,Chatbot,CloudformationChangeSet,CloudformationStack,CloudformationTemplate,Cloudformation,Cloudtrail,CloudwatchAlarm,CloudwatchEventEventBased,CloudwatchEventTimeBased,CloudwatchLogs,CloudwatchRule,Cloudwatch,Codeguru,CommandLineInterface,Config,ControlTower,LicenseManager,ManagedServices,ManagementAndGovernance,ManagementConsole,OpsworksApps,OpsworksDeployments,OpsworksInstances,OpsworksLayers,OpsworksMonitoring,OpsworksPermissions,OpsworksResources,OpsworksStack,Opsworks,OrganizationsAccount,OrganizationsOrganizationalUnit,Organizations,PersonalHealthDashboard,Proton,ServiceCatalog,SystemsManagerAppConfig,SystemsManagerAutomation,SystemsManagerDocuments,SystemsManagerInventory,SystemsManagerMaintenanceWindows,SystemsManagerOpscenter,SystemsManagerParameterStore, ParameterStore,SystemsManagerPatchManager,SystemsManagerRunCommand,SystemsManagerStateManager,SystemsManager, SSM,TrustedAdvisorChecklistCost,TrustedAdvisorChecklistFaultTolerant,TrustedAdvisorChecklistPerformance,TrustedAdvisorChecklistSecurity,TrustedAdvisorChecklist,TrustedAdvisor,WellArchitectedTool
        from diagrams.aws.media import ElasticTranscoder,ElementalConductor,ElementalDelta,ElementalLive,ElementalMediaconnect,ElementalMediaconvert,ElementalMedialive,ElementalMediapackage,ElementalMediastore,ElementalMediatailor, ElementalServer,KinesisVideoStreams,MediaServices    
        from diagrams.aws.migration import ApplicationDiscoveryService,ADS, CloudendureMigration, CEM, DatabaseMigrationService,DMS, DatasyncAgent, Datasync, MigrationAndTransfer,MAT, MigrationHub, ServerMigrationService,SMS, SnowballEdge,Snowball,Snowmobile,TransferForSftp 
        from diagrams.aws.ml import ApacheMxnetOnAWS,AugmentedAi,Bedrock,Comprehend,DeepLearningAmis,DeepLearningContainers,DLC,Deepcomposer,Deeplens,Deepracer,ElasticInference,Forecast,FraudDetector,Kendra,Lex,MachineLearning,Personalize,Polly,RekognitionImage,RekognitionVideo,Rekognition, SagemakerGroundTruth,SagemakerModel,SagemakerNotebook,SagemakerTrainingJob,Sagemaker,TensorflowOnAWS,Textract,Transcribe,Translate
        from diagrams.aws.mobile import Amplify,APIGatewayEndpoint,APIGateway,Appsync,DeviceFarm,Mobile,Pinpoint
        from diagrams.aws.network import APIGatewayEndpoint,APIGateway,AppMesh,ClientVpn,CloudMap,CloudFrontDownloadDistribution,CloudFrontEdgeLocation,CloudFrontStreamingDistribution,CloudFront, CF,DirectConnect,ElasticLoadBalancing, ELB,ElbApplicationLoadBalancer, ALB,ElbClassicLoadBalancer, CLB,ElbNetworkLoadBalancer, NLB,Endpoint,GlobalAccelerator, GAX,InternetGateway, IGW,Nacl,NATGateway,NetworkFirewall,NetworkingAndContentDelivery,PrivateSubnet,Privatelink,PublicSubnet,Route53HostedZone,Route53,RouteTable,SiteToSiteVpn,TransitGatewayAttachment, TGWAttach,TransitGateway, TGW,VPCCustomerGateway,VPCElasticNetworkAdapter,VPCElasticNetworkInterface,VPCFlowLogs,VPCPeering,VPCRouter,VPCTrafficMirroring,VPC,VpnConnection,VpnGateway
        from diagrams.aws.quantum impimport Braket,QuantumTechnologies
        from diagrams.aws.robotics import RobomakerCloudExtensionRos,RobomakerDevelopmentEnvironment,RobomakerFleetManagement,RobomakerSimulator,Robomaker,Robotics
        from diagrams.aws.satellite import GroundStation, Satellite
        from diagrams.aws.security import AdConnector,Artifact, CertificateAuthority, CertificateManager, ACM, CloudDirectory, Cloudhsm,CloudHSM,Cognito,Detective,DirectoryService, DS, FirewallManager, FMS,Guardduty,IdentityAndAccessManagementIamAccessAnalyzer,IAMAccessAnalyzer,IdentityAndAccessManagementIamAddOn, IdentityAndAccessManagementIamAWSStsAlternate,IdentityAndAccessManagementIamAWSSts,IAMAWSSts, IdentityAndAccessManagementIamDataEncryptionKey,IdentityAndAccessManagementIamEncryptedData,IdentityAndAccessManagementIamLongTermSecurityCredential,IdentityAndAccessManagementIamMfaToken, IdentityAndAccessManagementIamPermissions,IAMPermissions,IdentityAndAccessManagementIamRole,IAMRole,IdentityAndAccessManagementIamTemporarySecurityCredential,IdentityAndAccessManagementIam, IAM,InspectorAgent,Inspector,KeyManagementService, KMS, Macie,ManagedMicrosoftAd, ResourceAccessManager, RAM,SecretsManager,SecurityHubFinding,SecurityHub,SecurityIdentityAndCompliance, ShieldAdvanced,Shield,SimpleAd,SingleSignOn,WAFFilteringRule,WAF                                       
        from diagrams.aws.storage import Backup,CloudendureDisasterRecovery, CDR,EFSInfrequentaccessPrimaryBg,EFSStandardPrimaryBg,ElasticBlockStoreEBSSnapshot, ElasticBlockStoreEBSVolume, ElasticBlockStoreEBS, EBS,ElasticFileSystemEFSFileSystem, ElasticFileSystemEFS, EFS,FsxForLustre, FsxForWindowsFileServer, Fsx, FSx,MultipleVolumesResource,S3AccessPoints,S3GlacierArchive,S3GlacierVault,S3Glacier,S3ObjectLambdaAccessPoints,SimpleStorageServiceS3BucketWithObjects,SimpleStorageServiceS3Bucket,SimpleStorageServiceS3Object, SimpleStorageServiceS3,S3,SnowFamilySnowballImportExport,SnowballEdge, Snowball, Snowmobile,StorageGatewayCachedVolume,StorageGatewayNonCachedVolume, StorageGatewayVirtualTapeLibrary,StorageGateway, Storage
               
        Example of correct usage:
        ```python
        from diagrams import Diagram, Cluster
        from diagrams.aws.compute import EC2, Lambda
        from diagrams.aws.database import Dynamodb
        from diagrams.aws.network import ELB
        from diagrams.aws.storage import S3
        from diagrams.aws.management import Cloudwatch

        with Diagram("Example Architecture", show=True):
            ELB("Load Balancer") >> EC2("Web Server") >> Dynamodb("Database")
        
        Follow these rules: 
        1. Always use the official import structure from diagrams library documentation
        2. Specify the exact import path for each provider/service needed
        3. Include only the specific services/icons that will be used
        4. Follow this import pattern:
        - from diagrams import Diagram, Cluster
        - from diagrams.aws.[category] import [specific_service]
        - from diagrams.generic.[category] import [specific_item]
        etc.
        5. Create appropriate clusters for different layers (e.g., Network Layer, Application Layer, Data Layer)
        6. Add all relevant AWS services for the application
        7. Define connections between services and use () around nodes separated by dashes -
        8. Include proper configuration for the diagram (direction, filename, etc.)
        9. Cluster object cannot have links to each other
        10. Use '-' operator only if you have an explicit demand
        11. Check and remove double links except when explicitly required
        12. when connecting multiple services be sure to connect them one at a time or using for loops to avoid connection lists and getting errors
        

        For example, if we need EC2 and S3 services, use:
        from diagrams.aws.compute import EC2
        from diagrams.aws.storage import S3
        
        Example of generated python script for clustered web services:
        
        from diagrams import Cluster, Diagram
        from diagrams.aws.compute import ECS
        from diagrams.aws.database import ElastiCache, RDS
        from diagrams.aws.network import ELB
        from diagrams.aws.network import Route53
        
        with Diagram("Clustered Web Services", show=False):
            dns = Route53("dns")
            lb = ELB("lb")
        
            with Cluster("Services"):
                svc_group = [ECS("web1"),
                             ECS("web2"),
                             ECS("web3")]
        
            with Cluster("DB Cluster"):
                db_primary = RDS("userdb")
                db_primary - [RDS("userdb ro")]
        
            memcached = ElastiCache("memcached")
        
            dns >> lb 
            lb >> svc_group[0]
            lb >> svc_group[1]
            lb >> svc_group[2]
            
            svc_group[0] >> db_primary
            svc_group[1] >> db_primary
            svc_group[2] >> db_primary
            
            svc_group[0] >> memcached
            svc_group[1] >> memcached
            svc_group[2] >> memcached
        
        Example of generated python script for event processing on aws:
        
            from diagrams import Cluster, Diagram
            from diagrams.aws.compute import ECS, EKS, Lambda
            from diagrams.aws.database import Redshift
            from diagrams.aws.integration import SQS
            from diagrams.aws.storage import S3
            
            with Diagram("Event Processing", show=False):
                source = EKS("k8s source")
            
                with Cluster("Event Flows"):
                    with Cluster("Event Workers"):
                        workers = [ECS("worker1"),
                                   ECS("worker2"),
                                   ECS("worker3")]
            
                    queue = SQS("event queue")
            
                    with Cluster("Processing"):
                        handlers = [Lambda("proc1"),
                                    Lambda("proc2"),
                                    Lambda("proc3")]
            
                store = S3("events store")
                dw = Redshift("analytics")
            
                source >> workers[0]
                source >> workers[1]
                source >> workers[2]
                
                workers[0] >> queue
                workers[1] >> queue
                workers[2] >> queue
                
                queue >> handlers[0]
                queue >> handlers[1]
                queue >> handlers[2]
                
                handlers[0] >> store
                handlers[1] >> store
                handlers[2] >> store
                
                handlers[0] >> dw
                handlers[1] >> dw
                handlers[2] >> dw
                
        Example of generated python code for grouped workers on aws:
        
                from diagrams import Diagram
                from diagrams.aws.compute import EC2
                from diagrams.aws.database import RDS
                from diagrams.aws.network import ELB
                
                with Diagram("Grouped Workers", show=False, direction="TB"):
                    ELB("lb") >> EC2("worker1")
                    ELB("lb") >> EC2("worker2")
                    ELB("lb") >> EC2("worker3")
                    ELB("lb") >> EC2("worker4")
                    ELB("lb") >> EC2("worker5")
                    EC2("worker1") >> RDS("events")
                    EC2("worker2") >> RDS("events")
                    EC2("worker3") >> RDS("events")
                    EC2("worker4") >> RDS("events")
                    EC2("worker5") >> RDS("events")
        
        Please provide the Python code needed to create an aws architecture diagram for the following 
        {description} of the application. The output should be a complete, runnable Python script that generates a clear and professional AWS architecture diagram.
        """
        conversation = [{"role": "user","content": [{"text": prompt}],}]
        
        # Configure reasoning parameters with a 2000 token budget
        reasoning_config = {"thinking": {"type": "enabled","budget_tokens": 2000}} 
        
        # Send message and reasoning configuration to the model
        print("\nSending request to Amazon Bedrock (Claude 3.7)...")
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=conversation,
            additionalModelRequestFields=reasoning_config
        )

       # Extract token usage from response metadata
        token_usage = response['usage']
        
        # Log token usage
        print("Input Tokens:",token_usage['inputTokens'])
        print("Output Tokens:",token_usage['outputTokens'])
        print("Total Tokens:",token_usage['totalTokens'])
        
        #Optional: Save token usage to a log file
        with open(f"bedrock_token_usage_{tracking_number}.log", 'a') as log_file:
            import datetime
            log_file.write(f"{datetime.datetime.now()}: Input Tokens: {token_usage['inputTokens']}, Output Tokens: {token_usage['outputTokens']}, Total Tokens: {token_usage['totalTokens']}\n")
        
        # Extract the list of content blocks from the model's response
        content_blocks = response["output"]["message"]["content"]

        reasoning = None
        text = None

        # Process each content block to find reasoning and response text
        for block in content_blocks:
            if "reasoningContent" in block:
                reasoning = block["reasoningContent"]["reasoningText"]["text"]
            if "text" in block:
                text = block["text"]

        return reasoning, text

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)
        
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

# #####part to fix diagrams imports#########################
# Cache of all valid class locations: {class_name: full.module.path}
def build_aws_class_to_module_map():
    """Scan only AWS diagrams modules to map class names to their correct module paths."""
    class_to_module = {}
    for importer, modname, ispkg in pkgutil.walk_packages(path=diagrams_path, prefix="diagrams."):
        if not modname.startswith("diagrams.aws."):
            continue # skip non-AWS providers
        try:
            module = importlib.import_module(modname)
            for attr in dir(module):
                if attr[0].isupper():
                    # Only map if not already mapped (keeps first-found AWS class)
                    class_to_module.setdefault(attr, modname)
        except Exception:
            continue
    return class_to_module

def generate_diagram_script() -> str:
    """Generates a diagrams script with wrong module/class references."""
    return """from diagrams import Diagram
from diagrams.aws.compute import EC2, S3 # S3 is from the wrong module
from diagrams.aws.network import Route53Domain # This doesn't exist
from diagrams.aws.database import RDS

with Diagram("Example Architecture", direction="LR"):
dns = Route53Domain("DNS")
app = EC2("Web App")
storage = S3("Static Files")
db = RDS("Database")
dns >> app >> storage >> db
"""

def extract_imports(code: str):
    tree = ast.parse(code)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("diagrams"):
            for alias in node.names:
                imports.append((node.module, alias.name))
    return imports

def validate_and_fix_imports(code: str, class_map: dict):
    imports = extract_imports(code)
    code_lines = code.splitlines()
    replacements = {} # class_name -> (old_module, new_module)
    usage_corrections = {} # class_name -> corrected_name (if renamed)
    for module_path, class_name in imports:
        valid = False
        try:
            mod = importlib.import_module(module_path)
            if hasattr(mod, class_name):
                print(f"[VALID] {class_name} from {module_path}")
                valid = True
        except ModuleNotFoundError:
            print(f"[INVALID MODULE] {module_path}")
        except Exception as e:
            print(f"[ERROR] {module_path}: {str(e)}")
        if not valid:
            correct_module = class_map.get(class_name)
            if correct_module:
                print(f"[FIX] {class_name} should be imported from {correct_module}")
                replacements[class_name] = (module_path, correct_module)
            else:
                print(f"[UNKNOWN CLASS] {class_name} not found in diagrams.*")

    # Replace imports and usage
    for i, line in enumerate(code_lines):
        if line.strip().startswith("from diagrams"):
            for cls, (old_mod, new_mod) in replacements.items():
                if f"from {old_mod} import" in line and cls in line:
                    # Extract all class names in the line
                    all_classes = re.findall(r'\b\w+\b', line.split("import")[-1])
                    fixed_classes = [c for c in all_classes if c != cls]
                    if cls not in fixed_classes:
                        fixed_classes.append(cls)

                    # Update line to correct module and class list
                    code_lines[i] = f"from {new_mod} import {', '.join(fixed_classes)}"

    # Replace usages throughout the script
    full_code = "\n".join(code_lines)
    for cls, (old_mod, new_mod) in replacements.items():
        full_code = re.sub(rf'\b{cls}\b', cls, full_code)
    return full_code, bool(replacements)
####end section on repairing diagram imports

def save_diagram_script(full_code): #code
    """Save the generated Python script to a file"""
    script_path = f"generated_aws_diagram_{tracking_number}.py"
    
    with open(script_path, "w") as f:
        f.write(full_code) #code
    
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
        reasoning, text = invoke_bedrock_model(description)
        print("\n<thinking>")
        print(reasoning)
        print(text)
        if not text:
            print("Failed to generate diagram code. Exiting.")
            return
        
        # Step 3: Extract Python code
        python_code = extract_python_code(text)
        
        # Step 4: Save the user's description         
        description_path = f"aws_architecture_description_{tracking_number}.txt"
        with open(description_path, "w") as f:
            f.write(description)
        print(f"\nYour architecture description saved to: {description_path}")
        
        #step 4.5: check generated code for diagram import errors
        print("Building diagrams class map (this may take a few seconds)...")
        class_map = build_aws_class_to_module_map()
        code = generate_diagram_script()
        print("\nValidating and auto-correcting...")
        fixed_code, modified = validate_and_fix_imports(python_code, class_map)

        output_path = Path(f"generated_diagram{tracking_number}.py")
        output_path.write_text(fixed_code)
        print(f"\nScript written to {output_path}")
        if modified:
            print("One or more imports were corrected.")
        else:
            print("All imports and usages were valid.")
        
        # Step 5: Save the script
        #script_path = save_diagram_script(python_code)
        
        # Step 6: Ask if user wants to run the script
        #run_script = input("\nWould you like to run the script to generate the diagram? (y/n): ").lower()
        #if run_script == 'y':
         #   run_diagram_script(script_path)
        
        # Step 7: Ask if user wants to run the corrected script
        run2_script = input("\nWould you like to run the corrected script to generate the diagram? (y/n): ").lower()
        if run2_script == 'y':
            run_diagram_script(output_path)
            
        print("\nDone!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
