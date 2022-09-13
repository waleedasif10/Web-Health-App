import json
import boto3
import os

def lambda_handler(event, context):  
        
    DBName = os.environ.get("Waleed_API_DB")
    client = boto3.client('dynamodb')
    DB_client = boto3.resource('dynamodb')
    
    table= DB_client.Table(DBName)
    
    if event["httpMethod"] == "POST":
        
        requestBody = json.loads(event['body'])
        url         =    requestBody["URLS"]
        print(url)
        Item={
            "URLS": {'S': url}
        }
        client.put_item(
            TableName = DBName,
            Item=Item
        )
        response = {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200, 
                                "event[body]":event['body'],
                                "status":"put + url Inserted",
                                "list":"Values have been inserted"}),
            "isBase64Encoded": False
        }
        return response
    
    
    elif event["httpMethod"] == "GET":
        urllist = []
        print(event)
        tabledetails =  table.scan() 
        print(tabledetails)
        
        data = tabledetails['Items']
        
        for i in data:
            urllist.append(i["URLS"])
            
        response =  {
        "statusCode": 200,
        "body": json.dumps({"statusCode": 200,"httpMethod": event["httpMethod"] ,"status":"GET + url", "event[body]":urllist}),
        "isBase64Encoded": False
        }
        return response
        
        
    elif event["httpMethod"] == "PATCH": 
        
        old_url=event['body'].split(',')[0]
        new_url=event['body'].split(',')[1]
        print(old_url)
        print(new_url)
        
        Item={
            "URLS": {'S': new_url}
        }
        client.put_item(
            TableName = DBName,
            Item=Item
        )
          
        delete = client.delete_item(TableName = DBName,Key={
            'URLS': {'S': old_url}
        })
          

        return {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200, "event[body]":event['body'],
                                "status":"PATCH + url Inserted",
                                "list":new_url + " is added & " +old_url + "is deleted"}),
            "isBase64Encoded": False
            }
    
    elif event["httpMethod"] == "DELETE":
        details = json.loads(event['body'])
        print(json.loads(event['body']))
        url_val = details["URLS"]
        delete = client.delete_item(TableName = DBName,Key={
            'URLS': {'S': url_val}
        })
        
        response = {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200, "event[body]":details,
                                "status":"deleted url",
                                "list":"Value has been deleted"}),
            "isBase64Encoded": False
        }
        
        return response 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # client.query(
        #     TableName=DBName,
        #     KeyConditionExpression='URLS = :URLS',
        #     ExpressionAttributeValues={
        #         ':URLS': {'S': 'www.google.com'}
        #     }
        # )
        
        
        
        
        
        
        # response = {
        #     "statusCode": 200,
        #     "body": json.dumps({"statusCode": 200, 
        #                         "event[body]":event['queryStringParameters']}),
        #     "isBase64Encoded": False
        # }
        
        #         print('event:', json.dumps(event))
        
        # l = []

        # response = client.scan()
        # data = response['Items']
        
        # # data is a list of dictionaries
        # for i in data:
        #     l.append(i["url"])
        
        
        
        # urllist = [] 
        # table = client.scan()
        # response = client.get_item(TableName=DBName,Key={'S': "www.google.com"})
        
        
        
        
        
        
        
        
        
        
        
        
        
        # response = {
        #     'statusCode': 200,
        #     'body': json.dumps(event)
        # }
        
        # return response
        
        
        
        
        
        
        
        
        





    
