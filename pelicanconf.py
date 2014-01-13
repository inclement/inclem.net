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

# Uncomment for 'fork me on github' banner
#GITHUB_URL = 'https://github.com/inclement/inclem.net'

#THEME = 'notmyidea'
THEME = '../pelican-inclemnet-theme/'

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

OUTPUT_RETENTION = (".git", )

TYPOGRIFY = True

ARTICLE_URL = '{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
