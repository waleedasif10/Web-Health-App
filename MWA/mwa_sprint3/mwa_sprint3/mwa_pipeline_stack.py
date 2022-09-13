from aws_cdk import (
    # Duration
    Stack,
    pipelines as pipeline_,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions_ 

    # aws_sqs as sqs,
)
import aws_cdk as cdk
from constructs import Construct
from mwa_sprint3.mwa_pipeline_stage import MyStage

class MyPipelineStack(Stack):
       def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        source = pipeline_.CodePipelineSource.git_hub("waleedasif2022skipq/Pegasus_Python", "main",
        authentication= cdk.SecretValue.secrets_manager("my-tokenMWA"), trigger = actions_.GitHubTrigger('POLL')
         
        )

        synth=pipeline_.ShellStep("CodeBuild",
            input=source,
            commands=['cd MWA/mwa_sprint3/', 'npm install -g aws-cdk','pip install -r requirements.txt', 'cdk synth'],
            primary_output_directory = "MWA/mwa_sprint3/cdk.out"
        )

        unit_test = pipeline_.ShellStep("Codetest",
            commands= ["cd MWA/mwa_sprint3/ ", "pip install -r requirements.txt", "pytest"]
        )

        # Setting up Manual Approval for Prod Stage
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ManualApprovalStep.html
        manual_approval = pipeline_.ManualApprovalStep("MWAApprovalRequired")

        pipeline = pipeline_.CodePipeline(self, "MWAPipeline", synth= synth)

        beta = MyStage(self, "MWAbetaStage")
        prod = MyStage(self, "MWAProdStage")

        pipeline.add_stage(beta, pre= [unit_test] )
        pipeline.add_stage(prod, pre=[manual_approval])