import logging
import sys
import json
from pprint import pprint
import boto3
from rekognition_video import(RekognitionVideo)

logger = logging.getLogger()

def lambda_handler(event, context):
    setLogger()

    logger.info(f"Received {len(event['Records'])} messages.")
    for record in event['Records']:
        body = json.loads(record['body'])
        print(body)

        bucket_name = body['Records'][0]['s3']['bucket']['name']
        object_key = body['Records'][0]['s3']['object']['key']
        print(f"FilePath: {bucket_name}/{object_key}")

        # Analyze video
        rekognition_client = boto3.client("rekognition")
        video = RekognitionVideo.from_bucket(bucket_name, object_key, rekognition_client)
        print("Detecting labels in the video.")
        labels = video.do_label_detection()
        print(f"Detected {len(labels)} labels, here are the first twenty:")
        for label in labels[:20]:
            pprint(label.to_dict())

def setLogger():
    stdout_handler = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)

# if __name__ == "__main__":
#     lambda_handler(None, None)
