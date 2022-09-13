from aws_cdk import (
    # Duration
    Stack,
    aws_iam as iam,
    pipelines as pipeline_,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions_,
    aws_codebuild as aws_cb_,
    # aws_sqs as sqs,
)
import aws_cdk as cdk
from constructs import Construct
from mwa_sprint4.mwa_pipeline_stage import MyStage

class MyPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        pipeline_roles = self.create_role()
        source = pipeline_.CodePipelineSource.git_hub("waleedasif2022skipq/Pegasus_Python", "main",
        authentication= cdk.SecretValue.secrets_manager("my-tokenMWA"), trigger = actions_.GitHubTrigger('POLL')
         
        )

        synth=pipeline_.ShellStep("CodeBuild",
            input=source,
            commands=['cd MWA/mwa_sprint4/', 'npm install -g aws-cdk','pip install -r requirements.txt', 'cdk synth'],
            primary_output_directory = "MWA/mwa_sprint4/cdk.out"
        )

        unit_test = pipeline_.ShellStep("Codetest",
            commands= ['cd MWA/mwa_sprint4/ ','pip install -r requirements.txt', 'pip install -r requirements-dev.txt','pytest']
        )

        pyresttest = pipeline_.CodeBuildStep('pyrestdocker', commands=[],
            build_environment= aws_cb_.BuildEnvironment(
                build_image= aws_cb_.LinuxBuildImage.from_asset(self,"Image", directory="./docker-image").from_docker_registry(name="docker:dind"),
                privileged= True
            ),
            partial_build_spec= aws_cb_.BuildSpec.from_object(
                {
                "version": 0.2,
                "phases": {
                    "install": {
                    "commands": [
                        "nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &",
                        "timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\""
                    ]
                    },
                    "pre_build": {
                    "commands": [
                        "cd MWA/mwa_sprint4/docker-image",
                        "docker build -t api-test ."
                    ]
                    },
                    "build": {
                    "commands": [
                        "docker run api-test"
                    ]
                    }
                }
                }
            )
        )
        # Setting up Manual Approval for Prod Stage
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ManualApprovalStep.html
        manual_approval = pipeline_.ManualApprovalStep("MWAApprovalRequired")

        pipeline = pipeline_.CodePipeline(self, "MWAPipeline", synth= synth)

        beta = MyStage(self, "MWAbetaStage")
        prod = MyStage(self, "MWAProdStage")

        pipeline.add_stage(beta, pre= [unit_test], post=[pyresttest])
        pipeline.add_stage(prod, pre=[manual_approval])
        
        
        
    def create_role(self):  
            
        """
            Description: creating a function for defining a roles for pipeline
            
            Represents a principal that has multiple types of principals.
    
            A composite principal cannot have conditions. i.e. multiple 
            ServicePrincipals that form a composite principal 
            
            AWS service principals
            
            A service principal is an identifier for a service. 
            IAM roles that can be assumed by an AWS service are called service roles. 
            Service roles must include a trust policy. 
            Trust policies are resource-based policies attached to a role that defines 
            which principals can assume the role
            
            @param: self: scope(constructor)
            
            return: this function returns the roles for pipeline
        
        """
        role = iam.Role(self, "Pipeline-Role",
                      assumed_by=iam.CompositePrincipal(
                          iam.ServicePrincipal("lambda.amazonaws.com"),
                          iam.ServicePrincipal("sns.amazonaws.com"),
                          iam.ServicePrincipal("codebuild.amazonaws.com")),
                      managed_policies=
                      [
                        iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                        iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                        iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                        iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambdaInvocation-DynamoDB'),
                        
                        iam.ManagedPolicy.from_aws_managed_policy_name("AwsCloudFormationFullAccess"),
                        iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess"),
                        iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipeline_FullAccess"),
                        iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")                  
                        
                        ])
        return role
        

    # --------------------------------------------------------------------------    
