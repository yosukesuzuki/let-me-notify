# -*- coding: utf-8 -*-

from kay.generics import crud
from kay.routing import (
    ViewGroup, Rule
)

from core.models import CTNotification
from admin.forms import CTNotificationForm


class CTNotificationCRUDViewGroup(crud.CRUDViewGroup):
    model = CTNotification
    form = CTNotificationForm


view_groups = [
    ViewGroup(
        Rule('/', endpoint='index', view='admin.views.index'),
    ),
    CTNotificationCRUDViewGroup(),
]
