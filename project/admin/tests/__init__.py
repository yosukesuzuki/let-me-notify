# -*- coding: utf-8 -*-

from kay.ext.testutils.gae_test_base import GAETestBase

from core.models import CTNotification


class PutSGNotificationTest(GAETestBase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_put_sgnotification(self):
        entity = CTNotification(key_name='test1', title='test_title1')
        entity.put()
        entity_for_assert = CTNotification.get_by_key_name('test1')
        self.assertEquals(entity_for_assert.title, 'test_title1')
