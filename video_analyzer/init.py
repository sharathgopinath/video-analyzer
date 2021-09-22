import json
from video_analyzer.message_handler import MessageHandler
from video_analyzer.settings.dynamodb_settings import DynamoDbSettings

def lambda_handler(event, context):
    message_handler = MessageHandler(DynamoDbSettings())

    print(f"Received {len(event['Records'])} messages.")
    for record in event["Records"]:
        message = json.loads(record["body"])
        print(message)

        message_handler.handle(message)

# if __name__ == "__main__":
    # lambda_handler(None, None)
