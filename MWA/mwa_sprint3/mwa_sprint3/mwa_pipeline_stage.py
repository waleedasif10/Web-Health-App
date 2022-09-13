from aws_cdk import (
    # Duration,
    Stage,
    # aws_sqs as sqs,
)
import aws_cdk as cdk
from constructs import Construct
from mwa_sprint3.mwa_sprint3_stack import MwaSprint3Stack

class MyStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)    
        self.sprint3_stage = MwaSprint3Stack(self, "MWAStack")    