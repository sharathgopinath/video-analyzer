import datetime
import json
from typing import List
from decimal import Decimal
from video_analyzer.rekognition_objects import RekognitionFace
from video_analyzer.rekognition_video import RekognitionVideo
from video_analyzer.settings.boto3_session import Boto3Session
from video_analyzer.settings.dynamodb_settings import DynamoDbSettings
from boto3.dynamodb.types import TypeSerializer


class MessageHandler:
    def __init__(self, dynamoDbSettings: DynamoDbSettings, boto3_session: Boto3Session):
        self.dynamoDbSettings = dynamoDbSettings
        if (boto3_session is not None):
            self.boto3_session = boto3_session
        else:
            self.boto3_session = Boto3Session()

    def handle(self, message):
        bucket_name = message["bucket_name"]
        file_name = message["file_name"]
        cam_name = message["cam_name"]
        print(f"FilePath: {bucket_name}/{file_name}")

        dynamodb = self.boto3_session.get_client("dynamodb")
        todays_date = datetime.date.today()
        video_source_pk = f"video_source:{todays_date.year}:{todays_date.month}"
        response = dynamodb.get_item(TableName=self.dynamoDbSettings.table_name, Key = { "PK": {"S":video_source_pk} })
        file_names = []
        if ("Item" in response):
            file_names = response["Item"]["file_names"]
        
        if(file_name in file_names):
            print(f"File {file_name} already processed, skipping.")
            return

        file_names.append(file_name)

        # Analyze video
        rekognition_client = self.boto3_session.get_client("rekognition")
        video = RekognitionVideo.from_bucket(bucket_name, file_name, rekognition_client)
        print("Detecting labels in the video.")
        labels = video.do_label_detection()

        self.save_labels(labels, cam_name)

        self.save_video_source(self, file_names, video_source_pk, dynamodb)

    def save_labels(self, labels: List[RekognitionFace], cam_name: str):
        dynamodb = self.boto3_session.get_client("dynamodb")
        table_name = self.dynamoDbSettings.table_name
        typeSerializer = TypeSerializer()
        
        print (f"Saving {len(labels)} labels")
    
        todays_date = datetime.date.today()
    
        unique_labels = set([label.name for label in labels])
        label_pk = f"label:{todays_date.year}"
        label_sk = f"{todays_date.month}:{todays_date.day}"
        response = dynamodb.get_item(TableName=table_name, Key = { "PK": {"S":label_pk}, "SK": {"S":label_sk} })
        if ("Item" in response):
            existing_labels = set(response["Item"]["label_names"])
            unique_labels = existing_labels.union(unique_labels)
    
        dynamodb.update_item(
            TableName = table_name,
            Key = { "PK": {"S":label_pk}, "SK": {"S":label_sk} },
            UpdateExpression = "SET label_names = :vals",
            ExpressionAttributeValues = {
                ":vals": typeSerializer.serialize(unique_labels)
            }
        )
    
        for label in labels:
            pk_1 = f"label:{label.name}:{todays_date.year}"
            sk_1 = f"{todays_date.month}:{todays_date.day}:{cam_name}"
    
            dynamodb.update_item(
                TableName=table_name,
                Key = {
                    "PK": {"S":pk_1},
                    "SK": {"S":sk_1}
                },
                UpdateExpression="SET analysis_response = list_append(if_not_exists(analysis_response, :empty_list), :vals)",
                ExpressionAttributeValues={
                    ":vals": typeSerializer.serialize([json.loads(json.dumps(label.__dict__), parse_float=Decimal)]),
                    ":empty_list":typeSerializer.serialize([])
                }
            )

    def save_video_source(self, file_names:List[str], video_source_pk:str, dynamodb):
        typeSerializer = TypeSerializer()
        dynamodb.put_item(
            TableName = self.dynamoDbSettings.table_name,
            Item = {
                "PK":  {"S":video_source_pk },
                "file_names": typeSerializer.serialize(file_names)
            })