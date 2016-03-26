# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.security import ALL_PERMISSIONS

from .models import Post


class DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'read'),
        (Allow, Authenticated, 'comment'),
        (Allow, 'admin', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        self.request = request

