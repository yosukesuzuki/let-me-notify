# -*- coding: utf-8 -*-

from kay.generics import crud
from kay.routing import (
    ViewGroup, Rule
)

from core.models import CTNotification
from admin.forms import SGNotificationForm


class SGNotificationCRUDViewGroup(crud.CRUDViewGroup):
    model = CTNotification
    form = SGNotificationForm


view_groups = [
    ViewGroup(
        Rule('/', endpoint='index', view='admin.views.index'),
    ),
    SGNotificationCRUDViewGroup(),
]
