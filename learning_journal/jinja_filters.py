# coding=utf-8
from datetime import timezone


def dateformat(date):
    return date.strftime('%Y-%m-%d')


def datetimeformat(date):
    return date.strftime('%Y-%m-%d %I:%M %p')
