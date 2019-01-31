import boto3
try:
    ec2 = boto3.resource('ec2', region_name='eu-west-2')
    subnet = ec2.Subnet('subnet-cc5389b6')
    instances = subnet.create_instances(ImageId='ami-0664a710233d7c148', InstanceType='t2.micro',
                                        MaxCount=1,
                                        MinCount=1,
                                        KeyName='MyNewKeypair', SecurityGroups=[], SecurityGroupIds=['sg-08a437ed33a63bbb6'])
    print(instances)

except BaseException as exe:
    print(exe) 