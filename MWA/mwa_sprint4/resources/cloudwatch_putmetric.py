import boto3
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#client
class cloudWatchPutMetric:
    def __init__(self):
        self.client= boto3.client('cloudwatch')

    def put_data(self, nameSpace,metricName, dimension, value):
        response = self.client.put_metric_data(
            Namespace= nameSpace,
            MetricData=[
                {
                    'MetricName': metricName,
                    'Dimensions': dimension,
                    'Value': value
                },
            ]
        )
    
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Metric.html
    def create_metric(self, metric_name, namespace, dimensions, period):
        return self.client.Metric(metric_name=metric_name, 
                        namespace=namespace,
                        dimensions_map=dimensions,
                        period=period
                    )

    # # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html
    # def create_alarm(self, id_, comparison_operator, threshold, metric):
    #     return cloudwatch_.Alarm(self, id_,
    #                     comparison_operator=comparison_operator,
    #                     threshold=threshold,
    #                     evaluation_periods=1,
    #                     metric=metric
    #                 )

    
    def create_alarm(self,name, alarm_description, metricname, namespace, dimensions, threshold, sns_topic_arn, period = 60):

        return self.client.put_metric_alarm(
            AlarmName = name,
            AlarmDescription = alarm_description,
            ActionsEnabled=True,
            AlarmActions=[sns_topic_arn],
            MetricName = metricname,
            Namespace = namespace,  
            Statistic = 'Average',  #The statistic for the metric specified in MetricName
            Dimensions = dimensions,
            Period = period,        # The length, in seconds, used each time the metric specified in MetricName is evaluated. 10, 30, 60*. 
                                    # Be sure to specify 10 or 30 only for metrics that are stored by a PutMetricData call with a StorageResolution of 1.
            EvaluationPeriods = 1,  # Consecutive data point to breach threshold
            Threshold = threshold,  
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            )
    
    
    def delete_alarms(self,name):
        self.client.delete_alarms(
                AlarmNames=[name]
            )
        return True




