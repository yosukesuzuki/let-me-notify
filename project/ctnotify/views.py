# -*- coding: utf-8 -*-

import json

from werkzeug import Response

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from google.appengine.api import urlfetch
from google.appengine.ext import deferred

from kay.utils import render_to_response

from ctnotify.queue import get_process_que, get_sqs_connection, get_s3_object_key
from core.models import CTNotification, CTNotificationLog


def get_s3_object(aws_access_key_id, aws_secret_access_key, bucket_name, object_key):
    # remove later access key and id
    s3_connection = S3Connection(aws_access_key_id, aws_secret_access_key)
    bucket = s3_connection.get_bucket(bucket_name)
    s3_object = Key(bucket)
    s3_object.key = object_key
    s3_object_result = s3_object.get_contents_as_string()
    return s3_object_result


def parse_ctlog(json_data, filter_string):
    parse_result = []
    filters = filter_string.split(',')
    for ctlog in json_data['Records']:
        for filter in filters:
            if filter in ctlog['eventName']:
                parse_result.append({'event_name': ctlog['eventName'], 'ctlog': ctlog})
    return parse_result


def notify_to_slack(ctlogs, webhook_url):
    for ctlog in ctlogs:
        raw_content = '```\n' + json.dumps(ctlog['ctlog'], indent=4) + '\n```'
        payloads = json.dumps(
            {'text': raw_content, 'username': u'notify-bot'}, ensure_ascii=True)
        urlfetch.fetch(
            url=webhook_url,
            payload=payloads,
            method=urlfetch.POST,
            deadline=30,
            follow_redirects=False,
        )
        entity = CTNotificationLog(event_name=ctlog['event_name'], raw_content=raw_content)
        entity.put()


def check_ctlog(ct_setting):
    sqs_connection = get_sqs_connection(ct_setting.access_key_id, ct_setting.secret_access_key)
    parse_task_que = get_process_que(
        sqs_connection, ct_setting.que_name)
    if parse_task_que.count() > 0:
        fetch_que_result = sqs_connection.receive_message(parse_task_que)
        bucket_name, object_key = get_s3_object_key(fetch_que_result[0].get_body())
        ctlog = json.loads(get_s3_object(ct_setting.access_key_id, ct_setting.secret_access_key,
                                         bucket_name, object_key))
        parse_result = parse_ctlog(ctlog, ct_setting.event_name)
        notify_to_slack(parse_result, ct_setting.slack_webhook)
        parse_task_que.delete_message(fetch_que_result[0])
        deferred.defer(check_ctlog, ct_setting)


def index(request):
    ct_notif_settings = CTNotification.all().fetch(1000)
    for ct_setting in ct_notif_settings:
        check_ctlog(ct_setting)
    return Response('ok')
