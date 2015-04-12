# -*- coding: utf-8 -*-

from kay.routing import (
    ViewGroup, Rule
)

view_groups = [
    ViewGroup(
        Rule('/get_message', endpoint='get_message', view='ctnotify.views.get_message'),
        Rule('/', endpoint='index', view='ctnotify.views.index'),
    )
]
