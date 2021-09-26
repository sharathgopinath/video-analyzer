from video_analyzer.settings.aws_settings import AWSSettings
import boto3

class Boto3Session:
    def __init__(self, aws_settings: AWSSettings=None):
        self.aws_settings = aws_settings

    def get_client(self, aws_service:str):
        if self.aws_settings is None:
            return boto3.client(aws_service)

        boto3_session = boto3.Session(
            aws_access_key_id=self.aws_settings.aws_access_key_id,
            aws_secret_access_key=self.aws_settings.aws_secret_access_key,
            region_name=self.aws_settings.region_name
        )

        return boto3_session.client(
            service_name=aws_service,
            endpoint_url=self.aws_settings.endpoint_url,
            config=self.aws_settings.config)



