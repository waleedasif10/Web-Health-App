from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_ 
    # aws_sqs as sqs,
)
from constructs import Construct

class MwaSprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        waleed_lambda = self.create_lambda("WALEED_First_Function", 'hw_lambda.lambda_handler', "./resources")
        # example resource
        # queue = sqs.Queue(
        #     self, "MwaSprint1Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
    def create_lambda(self, id, handler, path):
        return lambda_.Function(self, id,
                        runtime=lambda_.Runtime.PYTHON_3_8,
                        handler=handler,
                        code=lambda_.Code.from_asset(path)
                    )
                