# -*- coding: utf-8 -*-

import os
import json
import gzip
from kay.ext.testutils.gae_test_base import GAETestBase

from core.models import CTNotification
from ctnotify.queue import get_sqs_connection, get_process_que, get_s3_object_key
from ctnotify.views import parse_ctlog

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


def _getTestingJSON(filename):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(
        module_dir, filename)
    json_file = open(file_path, 'rb')
    return json_file.read()


def _getGzipTestingJSON(filename):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(
        module_dir, filename)
    json_file = gzip.open(file_path, 'rb')
    return json_file.read()


class PutSGNotificationTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_put_sgnotification(self):
        entity = CTNotification(key_name='test1', title='test_title1')
        entity.put()
        entity_for_assert = CTNotification.get_by_key_name('test1')
        self.assertEquals(entity_for_assert.title, 'test_title1')


class SQSConnectionTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_sqs_connection(self):
        sqs_connection = get_sqs_connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        self.assertEquals(sqs_connection._provider_type, 'aws')
        get_process_que(sqs_connection, 'ctlog-notify')

    def test_connection_error(self):
        sqs_connection = get_sqs_connection('hoge', 'hage')
        self.assertEquals(sqs_connection._provider_type, 'aws')
        process_que = get_process_que(sqs_connection, 'ctlog-notify')
        self.assertEquals(process_que, False)


class ParseMessageTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_message_parse(self):
        # import pdb; pdb.set_trace()
        message_json = _getTestingJSON('sqs_body.json')
        bucket_name, object_key = get_s3_object_key(message_json)
        self.assertEquals(bucket_name, 'test-bucket')
        self.assertEquals(object_key, 'key-for-test')


class ParseCTLogTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_message_parse(self):
        # import pdb; pdb.set_trace()
        ctlog = json.loads(_getTestingJSON('dummy.ctlog.json'))
        parse_result = parse_ctlog(ctlog, 'SecurityGroupIngress')
        self.assertEquals(parse_result[0]['event_name'], 'AuthorizeSecurityGroupIngress')
