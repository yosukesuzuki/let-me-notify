# -*- coding: utf-8 -*-

from kay.utils.forms.modelform import ModelForm

from core.models import CTNotification


class SGNotificationForm(ModelForm):
    class Meta:
        model = CTNotification
