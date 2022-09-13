import aws_cdk as core
import aws_cdk.assertions as assertions

from mwa_sprint1.mwa_sprint1_stack import MwaSprint1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in mwa_sprint1/mwa_sprint1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MwaSprint1Stack(app, "mwa-sprint1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
