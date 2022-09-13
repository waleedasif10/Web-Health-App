
# Welcome to Sprint 1 readme!

This readme is a guide to how to get started with AWS CDK using Python. AWS CDK is an Infrastructure as Code tool that allows you to setup AWS resource through code.
Work on this repository was done on Linux.


## Setting up environment.

First update Linux (Ubuntu) and install Python
```
$ sudo apt update
$ sudo apt install python3 python3-pip
```

Install AWS CDK:
```
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
```

Install NVM and NPM
```
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
$ nano ~/.bash_profile
$ export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
$ source ~/.bash_profile
$ nvm ls-remote
$ nvm install v16.3.0 && nvm use v16.3.0 && nvm alias default v16.3.0
$ npm install -g aws-cdk
```

Configure your AWS settings
```
$ aws configure
```
Enter details from by going to IAM -> YourUserAccount -> Security Credentials


## Setting up the repo and AWS deployment.

First fork this repo, then clone it
```
$ git clone https://github.com/abdulrahman2022skipq/Pegasus_Python.git
```

Move into Pegasus_Python/ARJ/sprint1_arj directory, activate virtual env and install requirements.txt
```
$ cd Pegasus_Python/ARJ/sprint1_arj
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

At this point, you can edit the handler in `Pegasus_Python/ARJ/sprint1_arj/resources/hw_lambda.py` or you can just use the given code. 

At this point, you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

Now deploy this template on AWS.
```
$ cdk deploy
```

## Now test the Lambda Handler.
1. Go to, AWS Lambda on console and find your Lambda Function you deployed and click it.
2. Scroll down and have a look at you handler code.
3. Now configure a test and json request.
4. Run the test and check if lambda handler is working fine.


That's all from Week 1 Sprint.

## What we did in Sprint 1.
1. Setup environment.
2. Work on the github repo and write your own lambda handler.
3. Synthesis and deploy using `cdk synth` and `cdk deploy`.
4. Testing the deployed lambda function.

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!