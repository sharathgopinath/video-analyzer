import json
from pprint import pprint
import boto3
from rekognition_video import(RekognitionVideo)

def lambda_handler(event, context):
    print(f"Received {len(event['Records'])} messages.")
    for record in event['Records']:
        body = json.loads(record['body'])
        print(body)

        bucket_name = body['bucket_name']
        file_name = body['file_name']
        print(f"FilePath: {bucket_name}/{file_name}")

        # Analyze video
        rekognition_client = boto3.client("rekognition")
        video = RekognitionVideo.from_bucket(bucket_name, file_name, rekognition_client)
        print("Detecting labels in the video.")
        labels = video.do_label_detection()
        print(f"Detected {len(labels)} labels, here are the first twenty:")
        for label in labels[:20]:
            pprint(label.to_dict())


# if __name__ == "__main__":
#     lambda_handler(None, None)
