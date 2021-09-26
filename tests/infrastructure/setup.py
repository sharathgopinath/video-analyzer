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
        self.dynamodb_client = self.boto3_session.get_client("dynamodb")
        self.initialize()

    def initialize(self):
        self.cleanup_dynamodb()
        self.setup_dynamodb()

    def setup_dynamodb(self):
        self.dynamodb_client.create_table(
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
        try:
            self.dynamodb_client.delete_table(TableName=table_name)
        except Exception as ex:
            print(ex)
