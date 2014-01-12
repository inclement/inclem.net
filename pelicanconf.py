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

#PLUGINS = ['pelican_youtube', ]

STATIC_PATHS = ['media', 'images', ]

#PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

# Blogroll
LINKS = (('kivy.org', 'http://kivy.org/#home'),
         ('python.org', 'http://python.org/'))

# Social widget
SOCIAL = (('youtube', 'https://www.youtube.com/kivycrashcourse'),
          ('github', 'https://github.com/inclement'))

GITHUB_URL = 'https://github.com/inclement/inclem.net'

THEME = 'notmyidea'

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

OUTPUT_RETENTION = (".git", )

TYPOGRIFY = True
