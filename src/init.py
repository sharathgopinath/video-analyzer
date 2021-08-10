import logging
import sys

logger = logging.getLogger()

def lambda_handler(event, context):
    setLogger()

    logger.info(f"Received {len(event['Records'])} messages.")
    for record in event['Records']:
        payload = record["body"]
        logger.info(str(payload))

def setLogger():
    stdout_handler = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)

# if __name__ == "__main__":
#     lambda_handler(None, None)