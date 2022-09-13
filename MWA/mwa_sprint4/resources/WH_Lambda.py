import datetime
import urllib3 
import json
import boto3
import os
from cloudwatch_putmetric import cloudWatchPutMetric
from constants import *



def lambda_handler(event, context):
        # Obtains the latency and availability metrics for my websource
        watch = cloudWatchPutMetric()
        #DB  
        DBName = os.environ.get("Waleed_API_DB")
        client = boto3.client('dynamodb')
        DB_client = boto3.resource('dynamodb')
    
        table= DB_client.Table(DBName)
        # dictionary to return results as response
        table_values = []
        values = dict()
        # connect to CloudWatchMetric
        cw= cloudWatchPutMetric()  
        
        table_details =  table.scan()
        
        items = table_details['Items']
        
        for item in items:
            table_values.append(item["URLS"])
            
            
        for url in table_values:
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
            
            # Create Latency alarm for URLs
            watch.create_alarm(item[url] + "-Latency Alarm", 
                                "Latency Alarm for"+ item[url], 
                                URL_MONITOR_METRIC_NAME_LATENCY, 
                                URL_TO_NAMESPACE, 
                                dimensions, 
                                0.4,
                                SNS_TOPIC,
                                period = 60)
            
            # watch.create_metric(URL_MONITOR_METRIC_NAME_LATENCY, URL_TO_NAMESPACE, dimensions, Duration.minutes(1))

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
