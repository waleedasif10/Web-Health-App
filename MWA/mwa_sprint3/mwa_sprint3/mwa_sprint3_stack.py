from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_events as events_,
    aws_events_targets as target_,
    aws_cloudwatch as cloudwatch_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_cloudwatch_actions as cw_actions_,
    aws_sns_subscriptions as subscriptions_,
    aws_dynamodb as db_,
    aws_codedeploy as cd_,
    # aws_sqs as sqs,
)
from constructs import Construct
from resources.constants import *

class MwaSprint3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role = self.create_lambda_role()
        DBTable = self.create_table()
        
        # The code that defines your stack goes here
        waleed_lambda = self.create_lambda("WALEED_WH_Function", 'WH_Lambda.lambda_handler', "./resources", lambda_role)
         
        DBlambda = self.create_lambda("WALEED_DB", 'DynamoDBLambda.lambda_handler', "./resources", lambda_role)
        waleed_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        DBName = DBTable.table_name
        DBlambda.add_environment(key='Waleed_WH_DB', value=DBName)

        schedule= events_.Schedule.cron(minute="0")
        target =   target_.LambdaFunction(handler=waleed_lambda)
        # Automating the Lambda function
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events_targets/LambdaFunction.html
        rule = events_.Rule(self, "LambdaEventRule",    
            description = "This is to generate auto events for my WH_Lambda",
            schedule= schedule,
            targets=[target]
        )

        # Create SNS Topic 
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, 'AlarmNotification')
        topic.apply_removal_policy(RemovalPolicy.DESTROY)

        # Add SNS Subscription to SNS Topic
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.add_subscription(subscriptions_.EmailSubscription(EMAIL_ADDRESS))
        # topic.add_subscription(subscriptions_LambdaSubscription(DBlambda))
        topic.add_subscription(subscriptions_.LambdaSubscription(DBlambda))
        

        for url in URLS_TO_MONITOR:
            # Define thresholds and create Cloud Watch Alarms
            dimensions = {'URL': url}

            availMetric = self.create_metric(URL_MONITOR_METRIC_NAME_AVAILABILITY, URL_TO_NAMESPACE, dimensions, Duration.minutes(1))
            availAlarm = self.create_alarm(f'Availabilty_Alarm_{url}', cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD, 1, availMetric)
            availAlarm.add_alarm_action(cw_actions_.SnsAction(topic))
            availAlarm.apply_removal_policy(RemovalPolicy.DESTROY)

            latencyMetric = self.create_metric(URL_MONITOR_METRIC_NAME_LATENCY, URL_TO_NAMESPACE, dimensions, Duration.minutes(1))
            latencyAlarm = self.create_alarm(f'Latency_Alarm_{url}', cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 0.4, latencyMetric)
            latencyAlarm.add_alarm_action(cw_actions_.SnsAction(topic))
            latencyAlarm.apply_removal_policy(RemovalPolicy.DESTROY)

        # Setup Lambda Metrics Insights for Deployment (rollback incase of irregularities)
        mwa_lambda_duration = waleed_lambda.metric('Duration', period=Duration.minutes(60))

        mwa_lambda_invocations = waleed_lambda.metric('Invocations', period=Duration.minutes(60))

        # Setup Alarm for Lambda Insights
        mwa_lambda_duration_alarm = self.create_alarm('MWA_WH_Lambda_Duration_Alarm',
            cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 5500, mwa_lambda_duration
        )

        mwa_lambda_duration_alarm.apply_removal_policy(RemovalPolicy.DESTROY)

        mwa_lambda_invocations_alarm = self.create_alarm('MWA_WH_Lambda_Invocations_Alarm',
            cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 1, mwa_lambda_invocations
        )
        mwa_lambda_invocations_alarm.apply_removal_policy(RemovalPolicy.DESTROY)
        
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Alias.html
        version = waleed_lambda.current_version
        alias = lambda_.Alias(self, "MWA_WH_Lambda_Alias", alias_name="MWA_WH_Prod", version=version)
        
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html
        
        mwa_lambda_deployment = cd_.LambdaDeploymentGroup(self, "MWA_WH_Lambda_Deployment",
            alias=alias,
            alarms=[mwa_lambda_duration_alarm, mwa_lambda_invocations_alarm],
            deployment_config=cd_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
        )



    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
    def create_lambda(self, id, handler, path,role):
        return lambda_.Function(self, id,
                        runtime=lambda_.Runtime.PYTHON_3_8,
                        handler=handler,
                        code=lambda_.Code.from_asset(path),
                        timeout=Duration.seconds(15),
                        role=role
                    )

    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Metric.html
    def create_metric(self, metric_name, namespace, dimensions, period):
        return cloudwatch_.Metric(metric_name=metric_name, 
                        namespace=namespace,
                        dimensions_map=dimensions,
                        period=period
                    )

    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html
    def create_alarm(self, id_, comparison_operator, threshold, metric):
        return cloudwatch_.Alarm(self, id_,
                        comparison_operator=comparison_operator,
                        threshold=threshold,
                        evaluation_periods=1,
                        metric=metric
                    )



    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/Role.html
    def create_lambda_role(self):
        return iam_.Role(self, "lambda-role",
                        assumed_by=iam_.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                            iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')

                        ]
                    )
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html  
    def create_table(self):
        return db_.Table(self, id = "AlarmInfoTable",
            removal_policy =RemovalPolicy.DESTROY,
            
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Attribute.html#aws_cdk.aws_dynamodb.Attribute
            partition_key=db_.Attribute(name="AlarmName", type=db_.AttributeType.STRING))