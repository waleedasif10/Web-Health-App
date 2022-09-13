import aws_cdk as core
import aws_cdk.assertions as assertions

from mwa_sprint2.mwa_sprint2_stack import MwaSprint2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in mwa_sprint2/mwa_sprint2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MwaSprint2Stack(app, "mwa-sprint2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
