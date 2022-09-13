
# Welcome to your CDK Python project!
# Welcome to Sprint3 Readme!

This is a blank project for CDK development with Python.
This is a readme follows on how to get started with a CI/CD Pipeline Automation for Web Health App on AWS using Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.
Tech Stack: Python, [boto3 (AWS SDK)](https://aws.amazon.com/sdk-for-python/), [aws_cdk (AWS IaC)](https://docs.aws.amazon.com/cdk/api/v2/python/index.html)

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.
AWS Services used: [AWS Lambda](https://aws.amazon.com/lambda/), [AWS CloudWatch](https://aws.amazon.com/cloudwatch/), [AWS DynamoDB](https://aws.amazon.com/dynamodb/), [AWS SNS](https://aws.amazon.com/sns/), [AWS CodePipeline](https://aws.amazon.com/codepipeline/)

To manually create a virtualenv on MacOS and Linux:
## Setting up environment.

Follow the link to setup your environment: [Setup Environment](https://github.com/abdulrahman2022skipq/Pegasus_Python/tree/main/ARJ/sprint1_arj#readme)

## Setting up the repo and AWS deployment.

First fork this repo, then clone it
```
$ python3 -m venv .venv
$ git clone https://github.com/waleedasif2022skipq/Pegasus_Python.git
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

Move into Pegasus_Python/MWA/mwa_sprint2 directory, activate virtual env and install requirements.txt
```
$ cd Pegasus_Python/MWA/mwa_sprint2
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

If you are a Windows platform, you would activate the virtualenv like this:
At this point, everything is set up. All you may need to do is change the Names/Ids in the source code.

For the first time, you need to synthesize, git (add, commit, push) and deploy the app. After that, for any change you make in the code, you only need to git (add, commit, push) since then the pipeline itseld will detect changes and synthesize and deploy the app.

For the first time:
```
% .venv\Scripts\activate.bat
$ cdk synth
$ git add .
$ git commit -m "your commit"
$ git push
$ cdk deploy
```

Once the virtualenv is activated, you can install the required dependencies.

Once deployed, next time you only need the following commands:
```
$ pip install -r requirements.txt
$ git add .
$ git commit -m "your commit"
$ git push
```

At this point you can now synthesize the CloudFormation template for this code.
Congratulations, you have deployed your Web Health App CI/CD Pipeline.

```
$ cdk synth
```
## The App + Pipeline.

### Web Health App
Go to the [link](https://github.com/waleedasif2022skipq/Pegasus_Python/blob/main/MWA/mwa_sprint2/README.md) to know more about the app.

### CI/CD Pipeline
- For Source Stage, `aws_cdk.pipelines.CodePipelinesSource.git_hub()` is used.
- For Build Stage, `aws_cdk.pipelines.ShellStep()` is used.
- For Beta Stage, `mwa_sprint3.mwa_pipeline_stage.MyStage()` is used.
- For creating Unit Test in Beta Stage, `aws_cdk.pipelines.ShellStep()` is used.
- For Prod Stage, `mwa_sprint3.mwa_pipeline_stage.MyStage()` is used.
- For manual approval in Prod Stage, `aws_cdk.pipelines.ManualApprovalStep()` is used.
- To combine all stages in the pipeline, `aws_cdk.pipelines.CodePipeline` is used.

The `app.py` calls the pipeline, the pipeline calls the stage, the stage calls the stack.

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.
### Rollback & Lambda Insights
- For Lambda performance insights, Duration and Invocation metrics are used and corresponding alarms are created for them. Duration has to be greater than 5000 ms and more than 1 Invocation must be made within an hour for there alarms to be triggered.
- In case the alarms are trigged, the Pipeline is configure to rollback to its previous version using `aws_cdk.codedeploy.LambdaDeploymentGroup()`.

## Useful commands
That's all from Week 3 Sprint.

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
## What I did in Sprint 3.
1. Worked on an CI/CD Pipeline for Web Health App.
2. Created a Pipeline Stack using AWS CDK. This involved CodeSource Stage, CodeBuild Stage, Beta Stage (Unit Testing), Prod Stage (Manual Approval) and CodePipeline to combine all the stages into a single pipeline.
3. Wrote 5 unit tests in `tests/unit/test_mwa_sprint3_stack.py` using PyTest. Beta Stage takes care of Unit Testing.
4. For sending the app to production, you need to manually approve in the Prod Stage.
5. Created AWS Lambda Insight metrics in `mwa_sprint3/mwa_sprint3_stack.py` to check Lambda performance.
6. Alarm is generated in case the Lambda takes more times than allowed during execution or is invoked more than what is set using the Event Rule.
7. In case, an alarm is generated, AWS CodeDeploy is used to rollback the WH App to its previous version.
8. During this sprint, I got to learn about CI/CD Pipeline, role of AWS in it and various related concepts useful in DevOps.

Enjoy!