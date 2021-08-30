import datetime
from typing import List
from infrastructure.setup import *
from rekognition_objects import *
from rekognition_video import *
from init import *

from rekognition_objects import RekognitionLabel

def test_saves_labels():
    setup_dynamodb()

    labels:List[RekognitionLabel] = [
        RekognitionLabel({
            "Name": "Person",
            "Confidence": 90.222255588,
            "Instances": [],
            "Parents": []
        }, datetime.date.today())
    ]

    save(labels, "test_cam")
    