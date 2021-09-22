class AWSSettings:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, endpoint_url, config):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.endpoint_url = endpoint_url
        self.config = config