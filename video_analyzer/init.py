import json
from typing import List
import os
import datetime
from decimal import Decimal

from video_analyzer.rekognition_objects import RekognitionLabel
from video_analyzer.rekognition_video import(RekognitionVideo)
from video_analyzer.boto3_session import Boto3Session

table_name = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
    print(f"Received {len(event['Records'])} messages.")
    for record in event["Records"]:
        body = json.loads(record["body"])
        print(body)

        bucket_name = body["bucket_name"]
        file_name = body["file_name"]
        cam_name = body["cam_name"]
        print(f"FilePath: {bucket_name}/{file_name}")

        # Analyze video
        boto3_session = Boto3Session()
        rekognition_client = boto3_session.get_client("rekognition")
        video = RekognitionVideo.from_bucket(bucket_name, file_name, rekognition_client)
        print("Detecting labels in the video.")
        labels = video.do_label_detection()

        save(boto3_session, labels, cam_name)

def save(boto3_session: Boto3Session, labels: List[RekognitionLabel], cam_name: str):
    dynamodb = boto3_session.get_client("dynamodb")
    if (dynamodb is not None):
        print(table_name)
        return

    print (f"Saving {len(labels)} labels")

    todays_date = datetime.date.today()

    unique_labels = set([label.name for label in labels])
    label_pk = f"label:{todays_date.year}"
    label_sk = f"{todays_date.month}:{todays_date.day}"
    response = dynamodb.get_item(TableName=table_name, Key = { "PK": label_pk, "SK": label_sk })
    if ("Item" in response):
        existing_labels = set(response["Item"]["label_names"])
        unique_labels = existing_labels.union(unique_labels)

    dynamodb.update_item(
        TableName=table_name,
        Key = { "PK": label_pk, "SK": label_sk },
        UpdateExpression = "SET label_names = :vals",
        ExpressionAttributeValues = {
            ":vals": unique_labels
        }
    )

    for label in labels:
        pk_1 = f"label:{label.name}:{todays_date.year}"
        sk_1 = f"{todays_date.month}:{todays_date.day}:{cam_name}"

        dynamodb.update_item(
            TableName=table_name,
            Key = {
                "PK": pk_1,
                "SK": sk_1
            },
            UpdateExpression="SET analysis_response = list_append(if_not_exists(analysis_response, :empty_list), :vals)",
            ExpressionAttributeValues={
                ":vals": [json.loads(json.dumps(label.__dict__), parse_float=Decimal)],
                ":empty_list":[]
            }
        )

# if __name__ == "__main__":
    # lambda_handler(None, None)
