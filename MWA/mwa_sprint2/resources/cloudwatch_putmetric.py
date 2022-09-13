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




