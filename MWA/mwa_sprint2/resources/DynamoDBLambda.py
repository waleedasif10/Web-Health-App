import boto3
import os
import json

def lambda_handler(event, context):            
    #putting alarm details in DynamoDb table 

    #getting Dynamodb table name from Lambda enviroments variables
    DBName = os.environ.get("Waleed_WH_DB")
    client = boto3.client('dynamodb')
    
    # Loop over records in event
    for record in event['Records']:

        # Parse message key value from string to json
        message = json.loads(record['Sns']['Message'])

        # Parse and prepare item to put in DynamoDB Table
        # Data parsed from events: AlarmName, Timestamp, NewStateReason, MetricName, URL 
        item = {
            "AlarmName": {'S': message["AlarmName"]},
            "Timestamp": {'S': record['Sns']['Timestamp']},
            "NewStateReason": {'S': message["NewStateReason"]},
            "MetricName": {'S': message["Trigger"]["MetricName"]},
            "URL": {'S': message["Trigger"]["Dimensions"][0]["value"]},
        }        

        #put item in dynamo table
        response =  client.put_item(
            TableName = DBName,
            Item = item
        )

    return response