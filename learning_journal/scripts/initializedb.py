# coding=utf-8
from __future__ import unicode_literals

import os
import sys

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from ..models import (
    DBSession,
    Post,
    Base,
    User
    )
import transaction


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    settings = get_appsettings(config_uri, options=options)
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        password = os.environ.get('ADMIN_PASSWORD', 'admin')
        admin = User(username=u'admin', password=password)
        DBSession.add(admin)
