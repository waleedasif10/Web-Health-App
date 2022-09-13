import datetime
import urllib3 
from cloudwatch_putmetric import cloudWatchPutMetric
from constants import *


def lambda_handler(event, context):
        # Obtains the latency and availability metrics for my websource

        # dictionary to return results as response
        values = dict()
        # connect to CloudWatchMetric
        cw= cloudWatchPutMetric()  
        for url in URLS_TO_MONITOR:
            # Get availibility and latency for url
            availability = getAvailability(url)
            latency = getLatency(url)

            # set dimensions
            dimensions = [{
                'Name': 'URL',
                'Value': url
            }]
            
            # publish url results to CloudWatch
            responseAvail = cw.put_data(URL_TO_NAMESPACE, URL_MONITOR_METRIC_NAME_AVAILABILITY, dimensions, availability)
            responseLaten = cw.put_data(URL_TO_NAMESPACE, URL_MONITOR_METRIC_NAME_LATENCY, dimensions, latency)

            # update response
            values.update({url: {'availability': availability, 'latency': latency}})
        return values
def getLatency(url):
        # return latency time
        http = urllib3.PoolManager()
        start = datetime.datetime.now()
        response= http.request("GET", url)
        end = datetime.datetime.now()
        delta = end - start
        latencySec = round(delta.microseconds*.000001,6)
        return latencySec 
def getAvailability(url):
        # checks availability of a URL
        http = urllib3.PoolManager()
        response= http.request("GET",url)
        if response.status == 200:
            return 1.0
        else:
            return 0.0
