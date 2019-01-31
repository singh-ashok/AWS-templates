import boto3

ec2 = boto3.client('ec2')
response = ec2.create_key_pair(KeyName='KEY_PAIR_NAME')
print(response)