import logging
import sys
import json

logger = logging.getLogger()

def lambda_handler(event, context):
    setLogger()

    logger.info(f"Received {len(event['Records'])} messages.")
    for record in event['Records']:
        body = json.loads(record['body'])
        print(body)

        bucket_name = body['Records'][0]['s3']['bucket']['name']
        object_key = body['Records'][0]['s3']['object']['key']
        logger.info(f"FilePath: {bucket_name}/{object_key}")

def setLogger():
    stdout_handler = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)

# if __name__ == "__main__":
#     lambda_handler(None, None)