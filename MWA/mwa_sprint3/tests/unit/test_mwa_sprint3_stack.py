import aws_cdk as core
import aws_cdk.assertions as assertions

from mwa_sprint3.mwa_sprint3_stack import MwaSprint3Stack
import pytest

@pytest.fixture
def template():
    """
        Using @pytest.fixture so that you don't need to write boiler plate code for loading the template in each test.
    """
    app = core.App()
    stack = MwaSprint3Stack(app, "mwasprint3stack")
    template = assertions.Template.from_stack(stack)
    return template

def test_lambda_created(template):
    template.resource_count_is("AWS::Lambda::Function", 2)

def test_sns_created(template):
    template.resource_count_is("AWS::SNS::Subscription", 2)
    
def test_db_created(template):
    template.has_resource_properties("AWS::DynamoDB::Table",
        {
            "KeySchema": [
                {
                    "AttributeName": "AlarmName",
                    "KeyType": "HASH"
                }
            ],
            "AttributeDefinitions": [
                {
                    "AttributeName": "AlarmName",
                    "AttributeType": "S"
                }
            ],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }
    )
    
    
def test_iam_role_created(template):
    template.has_resource("AWS::IAM::Role",
        {
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Statement": [
                        {
                            "Action": "sts:AssumeRole",
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "lambda.amazonaws.com"
                            }
                        }
                    ],
                    "Version": "2012-10-17"
                },
                "ManagedPolicyArns": [
                    {
                        "Fn::Join": [
                            "",
                            [
                                "arn:",
                                {
                                    "Ref": "AWS::Partition"
                                },
                                ":iam::aws:policy/CloudWatchFullAccess"
                            ]
                        ]
                    },
                    {
                        "Fn::Join": [
                            "",
                            [
                                "arn:",
                                {
                                    "Ref": "AWS::Partition"
                                },
                                ":iam::aws:policy/AmazonDynamoDBFullAccess"
                            ]
                        ]
                    }
                ]
            }
        }
    )


