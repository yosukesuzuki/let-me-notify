# -*- coding: utf-8 -*-
# core.models

from google.appengine.ext import db

# Create your models here.


class CTNotification(db.Model):
    title = db.StringProperty(verbose_name='title')
    access_key_id = db.StringProperty(verbose_name='access key id')
    secret_access_key = db.StringProperty(verbose_name='secret access key')
    que_name = db.StringProperty(verbose_name='que name of notification from CloudTrail')
    event_name = db.StringProperty(verbose_name='Event Name, comma separated')
    slack_webhook = db.StringProperty(verbose_name='Incoming webhook URL')
    updated_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        return self.title


class CTNotificationLog(db.Model):
    event_name = db.StringProperty(verbose_name='Event Name, comma separated')
    raw_content = db.TextProperty(verbose_name='Content of notfication')
    updated_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
