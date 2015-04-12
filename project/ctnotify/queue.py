# -*- coding: utf-8 -*-

import json

from boto import sqs
from boto.exception import SQSError

from kay.conf import settings


def get_sqs_connection(access_key_id, secret_access_key):
    sqs_connection = sqs.connect_to_region(
        settings.AWS_REGION,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key)
    return sqs_connection


def get_process_que(sqs_connection, que_name):
    process_que = sqs_connection.get_queue(que_name)
    if process_que is None:
        try:
            sqs_connection.create_queue(que_name, 600)
        except SQSError:
            return False
        process_que = sqs_connection.get_queue(que_name)
    return process_que


def get_s3_object_key(message_json):
    ctlog_notification = json.loads(json.loads(message_json)['Message'])
    bucket_name = ctlog_notification['s3Bucket']
    object_key = ctlog_notification['s3ObjectKey'][0]
    return bucket_name, object_key
