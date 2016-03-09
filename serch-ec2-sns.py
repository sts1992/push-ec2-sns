
import json
import boto3

client = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):

    print('Loading function')
    response = client.describe_instances( Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'stopped'
                ]
            }
        ]
    )
    print(response)

    instance_ids = []
    instance_type = []
    info = []

    i = len(response['Reservations'])
    for a in range(0, i):
        instance_ids.insert(a, response['Reservations'][a]['Instances'][0]['InstanceId'])
        instance_type.insert(a, response['Reservations'][a]['Instances'][0]['InstanceType'])
        info.insert(a, {instance_ids[a]:instance_type[a]})


    topic = 'arn:aws:sns:ap-northeast-1:xxxxx'
    subject = 'Your Email Subject!!'

    response = sns.publish(
        TopicArn=topic,
        Message=str(info),
        Subject=subject,
    )

    return info
