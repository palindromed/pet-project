# coding=utf-8
import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .jinja_filters import dateformat, datetimeformat

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    database_url = os.environ.get('DATABASE_URL', None)
    if database_url:
        settings['sqlalchemy.url'] = database_url

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.commit()
    config.add_static_view('static', 'static', cache_max_age=3600)

    # jinja2 filters
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.filters['dateformat'] = dateformat
    jinja2_env.filters['datetimeformat'] = datetimeformat

    # routes
    config.add_route('list', '/')
    config.add_route('detail', '/post/{post_id:\d+}')


    config.scan()
    return config.make_wsgi_app()
