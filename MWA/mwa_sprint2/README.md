# Welcome to Sprint2 Readme!

This is a readme follows on how to get started with a Automated Web Health App on AWS using Python.

Tech Stack: Python, [boto3 (AWS SDK)](https://aws.amazon.com/sdk-for-python/), [aws_cdk (AWS IaC)](https://docs.aws.amazon.com/cdk/api/v2/python/index.html)

AWS Services used: [AWS Lambda](https://aws.amazon.com/lambda/), [AWS CloudWatch](https://aws.amazon.com/cloudwatch/), [AWS DynamoDB](https://aws.amazon.com/dynamodb/)

## Setting up environment.

Follow the link to setup your environment: [Setup Environment](https://github.com/waleedasif2022skipq/Pegasus_Python/tree/main/MWA/mwa_sprint1#readme)

## Setting up the repo and AWS deployment.

First fork this repo, then clone it
```
$ git clone https://github.com/waleedasif2022skipq/Pegasus_Python.git
```

Move into Pegasus_Python/MWA/mwa_sprint2 directory, activate virtual env and install requirements.txt
```
$ cd Pegasus_Python/MWA/mwa_sprint2
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

At this point, you can edit the following things:
1. Constants in `./resources/constants.py`. This includes: URLs, Email Address and Name Space
2. WH and DB Lambda Ids in `./mwa_sprint2/mwa_sprint2_stack.py`
3. DB Id and Enivronment Variable Name for DB Table in `./mwa_sprint2/mwa_sprint2_stack.py`
4. Rule Id and Schedule Cron in `./mwa_sprint2/mwa_sprint2_stack.py`
5. SNS Topic Name in `./mwa_sprint2/mwa_sprint2_stack.py`

Or, you can use the base settings.

At this point, you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

Now deploy this template on AWS.
```
$ cdk deploy
```

Congratulations, you have deployed your Web Health App.

## Testing the app.
### Web Health Lambda
1. Go to, AWS Lambda on console, find your WH Lambda Function you deployed, click it, scroll down and go to Monitor Tab.
2. Look at the logs, since this is an automated Lambda Handler, there will be a new event log every 1 minute (default).

### CloudWatch Metrics
1. Go to, AWS Cloud Watch on console, go to All Metrics from the sidebar, find your Metric NameSpace, click it and the URL Dimension, next you can checkbox any URL/Metric you want to view in the graph above.
2. Have a look at All Alarms from the sidebar, and see how many of your URLs are in OK or ALARM State.

### SNS Subscription
1. Since, you subscribed your email to SNS Topic, you will receive an email everytime any of the URLs go to ALARM State.
2. You also subsribed a Lambda Handler to your SNS Topic, so for each alarm, an event will be generated in the DB Lambda Function.

### DynamoDB Lambda
1. Go to, AWS Lambda on console, find your DB Lambda Function you deployed, click it, scroll down and go to Monitor Tab.
2. Look at the logs, there will be a new event log every time any of the URLs go to ALARM State.

### DynamoDB
1. Go to, AWS DynamoDB, and search your table.
2. Explore the table items. A new item is added to the table using the DB Lambda, everytime an alarm is generated.

That's all from Week 2 Sprint.

## What I did in Sprint 2.
1. Worked on an Automated Web Health App.
2. Created a Lambda Function that gets the availability and latency of a given URL and then puts these metrics in CloudWatch. Automated this Lambda to run every 1 minute.
3. Created an Alarm for every time a given metric crosses a certian threshold.
4. Used SNS Subscription to receive Email Notifications everytime an alarm was generated.
5. Used SNS Subscription to send an event to another Lambda Function everytime an alarm was generated.
6. The second Lambda Function parsed the event and extracted relevant information about the alarm. It then put the information in the DynamoDB Table.
7. All resources were created using aws_cdk in `mwa_sprint2_stack.py` file.
8. All resources were interacted in the Lambda Handlers using boto3.

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

Enjoy!
