import os
import boto3
import base64
import datetime
import pprint

def lambda_handler(event, context):

    # Read environment variables
    EC2_TAG_KEY = os.environ['EC2_TAG_KEY']
    EC2_TAG_VALUE = os.environ['EC2_TAG_VALUE']
    S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

    # A low-level client representing Amazon Elastic Compute Cloud (EC2)
    ec2 = boto3.client('ec2')

    # A low-level client representing Amazon Simple Storage Service (S3)
    s3 = boto3.client('s3')

    # A datetime object containing current date and time
    now = datetime.datetime.now()

    # Formate datetime as YYYYMMDD-HMS
    dt = now.strftime("%Y%m%d-%H%M%S")

    # Return instances which have specific tag key/value pair
    reservations = ec2.describe_instances(Filters=[
        {
            'Name': 'tag-key',
            'Values': [EC2_TAG_KEY, EC2_TAG_VALUE]
        },
    ]).get('Reservations', [])

    instances = sum(
    [
        [i for i in r['Instances']]
        for r in reservations
    ], [])

    print("Found %d instances that need to capture console screenshots" % len(instances))
    
    for instance in instances:
        InstanceName = [
            str(t.get('Value')) for t in instance['Tags']
            if t['Key'] == 'Name'][0]
        
        response = ec2.get_console_screenshot(
            DryRun=False,
            InstanceId=instance["InstanceId"],
            WakeUp=True
        )
        
        response = s3.put_object(
            Bucket = S3_BUCKET_NAME,
            Body = base64.b64decode(response["ImageData"]),
            Key = InstanceName + "/" + dt + ".jpg",
            ServerSideEncryption = 'AES256'
        )