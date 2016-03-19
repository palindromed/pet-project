# coding=utf-8
from __future__ import unicode_literals

from markdown import markdown as markdown_


def dateformat(date):
    if not date:
        return ""
    return date.strftime('%Y-%m-%d')


def datetimeformat(date):
    if not date:
        return ""
    return date.strftime('%Y-%m-%d %I:%M %p')


def markdown(text):
    if not text:
        return ""
    return markdown_(text)
