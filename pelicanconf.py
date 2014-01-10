#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Alexander Taylor'
SITENAME = u'inclem.net'
SITEURL = ''

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

PLUGINS = ['pelican_youtube', ]

STATIC_PATHS = ['media', 'images', ]

#PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

# Blogroll
LINKS = (('kivy.org', 'http://kivy.org/#home'),
         ('python.org', 'http://python.org/'))
# LINKS =  (('Pelican', 'http://getpelican.com/'),
#           ('Python.org', 'http://python.org/'),
#           ('Jinja2', 'http://jinja.pocoo.org/'),

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)
SOCIAL = (('youtube', 'https://www.youtube.com/kivycrashcourse'), )

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

OUTPUT_RETENTION = (".git", )

