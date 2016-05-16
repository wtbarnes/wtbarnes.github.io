#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

THEME='themes/pelican-themes/pelican-bootstrap3'
BOOTSTRAP_THEME='readable'
PYGMENTS_STYLE='emacs'

DISPLAY_CATEGORIES_ON_MENU=False

AUTHOR = u'Will Barnes'
SITENAME = u'Will Barnes'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

#path config
STATIC=['images','notebooks']
STATIC_PATHS=['images','notebooks']
ARTICLE_EXCLUDES=['notebooks']

#markup options
MARKUP=('md','ipynb')

#plugins
PLUGIN_PATHS=['pelican-plugins','plugins']
PLUGINS=['liquid_tags.notebook','pelican-ipynb.liquid',]#'pelican-ipynb.markdown']

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/wtbarnes_'),
          ('github', 'https://github.com/wtbarnes'),
          ('stackoverflow', 'http://stackoverflow.com/users/4717663/will-barnes', 'stack-overflow'))

# About Me blurb
AVATAR='/images/about_me.png'
ABOUT_ME='PhD student at Rice University studying plasma processes in million-degree solar coronal loops.'

#banner
BANNER='images/sdo_aia_171_loops_banner.png'

# Github
GITHUB_USER='wtbarnes'
GITHUB_REPO_COUNT=3
GITHUB_SKIP_FORK=False
#GITHUB_SHOW_USER_LINK=False

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#Article and page pretty urls
ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
