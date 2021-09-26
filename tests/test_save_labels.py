import datetime
from decimal import Decimal
from typing import List

from boto3.dynamodb.types import TypeDeserializer
from video_analyzer.message_handler import MessageHandler
from infrastructure.setup import *
from video_analyzer.rekognition_objects import RekognitionLabel
from pprint import pprint

TestContext.__test__ = False

def test_saves_labels():
    test_context = TestContext()

    labels:List[RekognitionLabel] = [
        RekognitionLabel({
            "Name": "Person",
            "Confidence": 90.222255588,
            "Instances": [],
            "Parents": []
        }),
        RekognitionLabel({
            "Name": "Stairs",
            "Confidence": 94.222255588,
            "Instances": [],
            "Parents": []
        })
    ]
    
    message_handler = MessageHandler(test_context.dynamoDbSettings)
    message_handler.save(test_context.boto3_session, labels, "test_cam")

    todays_date = datetime.date.today()
    label_pk = f"label:{todays_date.year}"
    label_sk = f"{todays_date.month}:{todays_date.day}"

    unique_labels_response = test_context.dynamodb_client.get_item(
        TableName=test_context.dynamoDbSettings.table_name, 
        Key = { "PK": {"S":label_pk}, 
        "SK": {"S":label_sk} }
    )

    analysis_response = test_context.dynamodb_client.get_item(
        TableName=test_context.dynamoDbSettings.table_name, 
        Key = { "PK": {"S":f"label:{labels[0].name}:{todays_date.year}"}, 
        "SK": {"S":f"{todays_date.month}:{todays_date.day}:test_cam"} }
    )
    typeSerializer = TypeDeserializer()

    assert unique_labels_response != None
    assert "Person" in unique_labels_response["Item"]["label_names"]["SS"]
    assert "Stairs" in unique_labels_response["Item"]["label_names"]["SS"]
    
    analysis = typeSerializer.deserialize(analysis_response["Item"]["analysis_response"])
    assert analysis[0]["confidence"] == Decimal('90.222255588')