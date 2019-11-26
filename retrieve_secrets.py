"""
Retrieve secrets from AWS secret manager and create file ready for sourcing in
relevant environment.
"""
import boto3
import os
import json
import sys
from botocore.exceptions import ClientError

REGION_NAME = "us-west-2"
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=REGION_NAME
)

def get_secrets(secret_name, output_file, json_flag=False):
    """
    Given a secret_name corresponding to the secrets on Secrets Manager in AWS,
    retrieve the secret and write it to the given output fileself.

    If the "json_flag" flag is set to True then a JSON object will be retrieved and
    each key/value pair will be written to a file in the format
    "export <key>=<value>\n".

    Otherwise, the secret will be treated as plain text and written directly to
    the specified output file with no extra processing.
    """
    try:
        secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        if json_flag:
            # json object of secrets, create script that will export each as env var
            secret_env_vars = json.loads(secret_value_response['SecretString'])
            with open(output_file, 'w+') as file:
                file.write("#!/bin/bash" + "\n")

                for env_var in secret_env_vars:
                    file.write("export " + env_var['ENV_VAR_NAME'] + "=" + env_var['VALUE'] + "\n")
        else:
            # plain text secret, create file from the plain text secret (probably a full script secret)
            with open(output_file, 'w+') as file:
                file.write(secret_value_response['SecretString'])

    except Exception as e:
        print("Failed to retrieve secrets. Exception: %s", e)
        raise e

if __name__ == '__main__':
    secret_name = sys.argv[1]
    output_file = sys.argv[2]
    json_flag = True if sys.argv[3] == "json" else False

    get_secrets(secret_name, output_file, json_flag)
