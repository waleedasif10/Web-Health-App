import pytest
import aws_cdk as core
import aws_cdk.assertions as assertions

from mwa_sprint4.mwa_sprint4_stack import MwaSprint4Stack



@pytest.fixture
def template():
    """
        Using @pytest.fixture so that you don't need to write boiler plate code for loading the template in each test.
    """
    app = core.App()
    stack = MwaSprint4Stack(app, "mwasprint4stack")
    template = assertions.Template.from_stack(stack)
    return template

def test_lambda_created(template):

    template.resource_count_is("AWS::Lambda::Function",3)
    
#Test to check creation of DBTable
def test_dbtable_created(template):


    template.resource_count_is("AWS::DynamoDB::Table",2)

    
    
 #test to check sns creation   
def test_sns_topic_created( template):

     template.resource_count_is("AWS::SNS::Topic", 1)

