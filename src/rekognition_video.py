# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from rekognition_objects import (
    RekognitionFace, RekognitionLabel, RekognitionPerson)

logger = logging.getLogger(__name__)

class RekognitionVideo:
    """
    Encapsulates an Amazon Rekognition video. This class is a thin wrapper around
    parts of the Boto3 Amazon Rekognition API.
    """
    def __init__(self, video, video_name, rekognition_client):
        """
        Initializes the video object.

        :param video: Amazon S3 bucket and object key data where the video is located.
        :param video_name: The name of the video.
        :param rekognition_client: A Boto3 Rekognition client.
        """
        self.video = video
        self.video_name = video_name
        self.rekognition_client = rekognition_client
        self.topic = None
        self.queue = None
        self.role = None

    @classmethod
    def from_bucket(cls, s3_object, rekognition_client):
        """
        Creates a RekognitionVideo object from an Amazon S3 object.

        :param s3_object: An Amazon S3 object that contains the video. The video
                          is not retrieved until needed for a later call.
        :param rekognition_client: A Boto3 Rekognition client.
        :return: The RekognitionVideo object, initialized with Amazon S3 object data.
        """
        video = {'S3Object': {'Bucket': s3_object.bucket_name, 'Name': s3_object.key}}
        return cls(video, s3_object.key, rekognition_client)
