## Lambda function to capture EC2 console screenshots and save it in a S3 bucket every 15 minutes.

### Configure triggers using CloudWatch events

* Schedule expression: rate(15 minutes)
* Enabled
    
### Programming language

* **Python** 3.7

### Environment variables

| KEY             | VALUE               |
| --------------- | ------------------- |
| S3_BUCKET_NAME  | console-screenshots |
| TAG_KEY         | screenshot          |
| TAG_VALUE       | true                |

### Create a custom role

* **Role Name:** lambda-capture-ec2-console-screenshots

Use lambda-capture-ec2-console-screenshots.json policy document to allow lambda function to capture and save screenshots in a S3 bucket.       

### Set Timeout

Set the Timeout to 30 seconds. This value might need to be changed according to your requirnments.
    
### Room for improvements

If you think you can further improve this function, feel free to send a PR.

### References

* [aws-lambda-console-accessing-environment-variables](https://www.radishlogic.com/aws/aws-lambda-console-accessing-environment-variables-via-python/)
* [Lambda function to check if specific tag do NOT exists-python](https://intellipaat.com/community/27965/lambda-function-to-check-if-specific-tag-do-not-exists-python)
* [Creation of snapshots using AWS Lambda](https://stackoverflow.com/questions/40421437/creation-of-snapshots-using-aws-lambda)
