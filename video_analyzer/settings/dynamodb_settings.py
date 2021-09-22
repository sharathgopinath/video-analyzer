import os

class DynamoDbSettings:
    def __init__(self, table_name:str = None):
        self.table_name = table_name if not None else os.environ.get("TABLE_NAME")