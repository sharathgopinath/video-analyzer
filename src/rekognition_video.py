# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import json
from pprint import pprint
import boto3
import os
from botocore.exceptions import ClientError
from rekognition_objects import (
    RekognitionFace, RekognitionLabel, RekognitionPerson)

job_queue_url = os.environ.get("JOB_QUEUE_URL")
job_topic_arn = os.environ.get("JOB_TOPIC_ARN")
job_role_arn = os.environ.get("JOB_ROLE_ARN")

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

        queue_client = boto3.resource('sqs')
        self.queue = queue_client.Queue(job_queue_url)

    @classmethod
    def from_bucket(cls, bucket_name, key, rekognition_client):
            """
            Creates a RekognitionVideo object from an Amazon S3 object.

            :param s3_object: An Amazon S3 object that contains the video. The video
                              is not retrieved until needed for a later call.
            :param rekognition_client: A Boto3 Rekognition client.
            :return: The RekognitionVideo object, initialized with Amazon S3 object data.
            """
            video = {'S3Object': {'Bucket': bucket_name, 'Name': key}}
            return cls(video, key, rekognition_client)

    def poll_notification(self, job_id):
        """
        Polls the notification queue for messages that indicate a job has completed.

        :param job_id: The ID of the job to wait for.
        :return: The completion status of the job.
        """
        status = None
        job_done = False
        while not job_done:
            messages = self.queue.receive_messages(
                MaxNumberOfMessages=1, WaitTimeSeconds=5)
            logger.info("Polled queue for messages, got %s.", len(messages))
            if messages:
                message = json.loads(messages[0].body)
                if job_id != message['JobId']:
                    continue
                status = message['Status']
                logger.info("Got message %s with status %s.", message['JobId'], status)
                messages[0].delete()
                job_done = True
        return status

    def _start_rekognition_job(self, job_description, start_job_func):
        """
        Starts a job by calling the specified job function.

        :param job_description: A description to log about the job.
        :param start_job_func: The specific Boto3 Rekognition start job function to
                               call, such as start_label_detection.
        :return: The ID of the job.
        """
        try:
            response = start_job_func(
                Video=self.video, NotificationChannel=self.get_notification_channel())
            job_id = response['JobId']
            logger.info(
                "Started %s job %s on %s.", job_description, job_id, self.video_name)
        except ClientError:
            logger.exception(
                "Couldn't start %s job on %s.", job_description, self.video_name)
            raise
        else:
            return job_id

    def _get_rekognition_job_results(self, job_id, get_results_func, result_extractor):
        """
        Gets the results of a completed job by calling the specified results function.
        Results are extracted into objects by using the specified extractor function.

        :param job_id: The ID of the job.
        :param get_results_func: The specific Boto3 Rekognition get job results
                                 function to call, such as get_label_detection.
        :param result_extractor: A function that takes the results of the job
                                 and wraps the result data in object form.
        :return: The list of result objects.
        """
        try:
            response = get_results_func(JobId=job_id)
            logger.info("Job %s has status: %s.", job_id, response['JobStatus'])
            results = result_extractor(response)
            logger.info("Found %s items in %s.", len(results), self.video_name)
        except ClientError:
            logger.exception("Couldn't get items for %s.", job_id)
            raise
        else:
            return results

    def _do_rekognition_job(
            self, job_description, start_job_func, get_results_func, result_extractor):
        """
        Starts a job, waits for completion, and gets the results.

        :param job_description: The description of the job.
        :param start_job_func: The Boto3 start job function to call.
        :param get_results_func: The Boto3 get job results function to call.
        :param result_extractor: A function that can extract the results into objects.
        :return: The list of result objects.
        """
        job_id = self._start_rekognition_job(job_description, start_job_func)
        status = self.poll_notification(job_id)
        if status == 'SUCCEEDED':
            results = self._get_rekognition_job_results(
                job_id, get_results_func, result_extractor)
        else:
            results = []
        return results

    def get_notification_channel(self):
        """
        Gets the role and topic ARNs that define the notification channel.

        :return: The notification channel data.
        """
        return {'RoleArn': job_role_arn, 'SNSTopicArn': job_topic_arn}

    def do_label_detection(self):
        """
        Performs label detection on the video.

        :return: The list of labels found in the video.
        """
        return self._do_rekognition_job(
            "label detection",
            self.rekognition_client.start_label_detection,
            self.rekognition_client.get_label_detection,
            lambda response: [
                RekognitionLabel(label['Label'], label['Timestamp']) for label in
                response['Labels']])
