from typing import List
from video_analyzer.message_handler import MessageHandler
from infrastructure.setup import *
from video_analyzer.rekognition_objects import RekognitionLabel

TestContext.__test__ = False

def test_saves_labels():
    test_context = TestContext()

    labels:List[RekognitionLabel] = [
        RekognitionLabel({
            "Name": "Person",
            "Confidence": 90.222255588,
            "Instances": [],
            "Parents": []
        })
    ]
    
    message_handler = MessageHandler(test_context.dynamoDbSettings)
    message_handler.save(test_context.boto3_session, labels, "test_cam")