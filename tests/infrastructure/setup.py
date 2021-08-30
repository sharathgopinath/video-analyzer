import boto3
import botocore

aws_access_key_id=""
aws_secret_access_key=""
region_name="ap-southeast-2"
endpoint_url='http://localhost:4566'
CONFIG = botocore.config.Config(retries={'max_attempts': 5})

def get_boto3_client(aws_service: str):
    return boto3.client(
        service_name=aws_service,
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=CONFIG)

def setup_dynamodb():
    dynamodb_client = get_boto3_client("dynamodb")
    dynamodb_client.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "PK",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SK",
                "AttributeType": "S"
            }
        ],
        TableName="video-analyzer",
        KeySchema=[
            {
                "AttributeName": "PK",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "SK",
                "KeyType": "RANGE"
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )

def cleanup_dynamodb():
    dynamodb_client = get_boto3_client("dynamodb")
    dynamodb_client.delete_table(TableName="video-analyzer")