import boto3
import datetime
import pprint
import base64
#import sys
#import collections

ec2 = boto3.client('ec2')

s3 = boto3.client('s3')

# datetime object containing current date and time
now = datetime.datetime.now()

# YYYY/MM/DD-HMS
dt_string = now.strftime("%Y%m%d-%H%M%S")

def lambda_handler(event, context):

    reservations = ec2.describe_instances(Filters=[
        {
            'Name': 'tag-key',
            'Values': ['screenshot', 'true']
        },
    ]).get('Reservations', [])

    instances = sum([[i for i in r['Instances']] for r in reservations], [])

    print("Found %d instances that need to capture console screenshots" % len(instances))
    
    for instance in instances:
        InstanceName = [
            str(t.get('Value')) for t in instance['Tags']
            if t['Key'] == 'Name'][0]
        #print (InstanceName)
        
        #print(instance["InstanceId"])
        
        response = ec2.get_console_screenshot(
            DryRun=False,
            InstanceId=instance["InstanceId"],
            WakeUp=True
        )
        #print(response["ImageData"])
        
        #picture = base64.b64decode(response["ImageData"])
        
        response = s3.put_object(
	        Bucket = 'yasitha-test',
	        Body = base64.b64decode(response["ImageData"]),
	        Key = InstanceName + "/" + dt_string + ".jpg",
            ServerSideEncryption = 'AES256'
        )