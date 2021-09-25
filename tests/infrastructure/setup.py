from video_analyzer.settings.dynamodb_settings import DynamoDbSettings
from video_analyzer.settings.aws_settings import AWSSettings
import botocore
from video_analyzer.settings.boto3_session import Boto3Session
import os

if "LOCALSTACK_HOST" in os.environ:
    localstack_host = os.environ.get("LOCALSTACK_HOST")
else:
    localstack_host = "localhost"

aws_access_key_id="123"
aws_secret_access_key="123"
region_name="ap-southeast-2"
endpoint_url=f"http://{localstack_host}:4566"
table_name="video-analyzer-test"
CONFIG = botocore.config.Config(retries={'total_max_attempts': 10})

class TestContext:
    def __init__(self):
        self.boto3_session = Boto3Session(
            aws_settings=AWSSettings(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
                endpoint_url=endpoint_url,
                config=CONFIG
            )
        )
        self.dynamoDbSettings = DynamoDbSettings(table_name)
        self.initialize()

    def initialize(self):
        self.setup_dynamodb()

    def setup_dynamodb(self):
        dynamodb_client = self.boto3_session.get_client("dynamodb")
        existing_tables = dynamodb_client.list_tables()['TableNames']
        if (table_name in existing_tables):
            print(f"Table {table_name} already exists")
            return

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
            TableName=table_name,
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
    
    def cleanup_dynamodb(self):
        dynamodb_client = self.boto3_session.get_client("dynamodb")
        dynamodb_client.delete_table(TableName=table_name)


# def get_boto3_client(aws_service: str):
#     return boto3.client(
#         service_name=aws_service,
#         endpoint_url=endpoint_url,
#         region_name=region_name,
#         aws_access_key_id=aws_access_key_id,
#         aws_secret_access_key=aws_secret_access_key,
#         config=CONFIG)

# def setup_test_context():
#     os.environ["TABLE_NAME"] = table_name
#     setup_dynamodb()

# def cleanup_dynamodb():
#     dynamodb_client = get_boto3_client("dynamodb")
#     dynamodb_client.delete_table(TableName=table_name)