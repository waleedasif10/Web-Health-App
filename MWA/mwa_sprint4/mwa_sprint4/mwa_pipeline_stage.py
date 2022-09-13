from aws_cdk import (
    # Duration,
    Stage,
    # aws_sqs as sqs,
)
import aws_cdk as cdk
from constructs import Construct
from mwa_sprint4.mwa_sprint4_stack import MwaSprint4Stack

class MyStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)    
        self.sprint4_stage = MwaSprint4Stack(self, "MWAStack")    