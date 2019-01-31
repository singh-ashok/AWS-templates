import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

try:
    allocation = ec2.allocate_address(Domain='vpc')
    response = ec2.associate_address(AllocationId=allocation['AllocationId'],
                                     InstanceId='INSTANCE_ID')
    print(response)
except ClientError as e:
    print(e)
 