import os

class DynamoDbSettings:
    def __init__(self, table_name:str = None):
        if table_name is not None:
            self.table_name = table_name
        else:
            self.table_name = os.environ.get("TABLE_NAME")