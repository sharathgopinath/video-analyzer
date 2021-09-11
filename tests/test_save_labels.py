import datetime
from typing import List
from video_analyzer.init import save
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
        }, datetime.date.today())
    ]
    
    save(test_context.boto3_session, labels, "test_cam")