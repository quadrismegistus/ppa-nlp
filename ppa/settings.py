"""
Django settings for ppa project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'sitemedia'),
]

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django_cas_ng',
    'pucas',
    'semanticuiforms',
    'webpack_loader',
    # 'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    # 'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    # 'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',
    'fullurl',
    'ppa.archive',
    'ppa.common',
    'ppa.unapi',
    'ppa.pages',
    'ppa.editorial',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'csp.middleware.CSPMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

ROOT_URLCONF = 'ppa.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates")
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ppa.context_extras',
                'ppa.context_processors.template_globals',
            ],
            'loaders': [
                'apptemplates.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

WSGI_APPLICATION = 'ppa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'sitemedia'),
    os.path.join(BASE_DIR, 'bundles'),
]

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, *MEDIA_URL.strip("/").split("/"))


SITE_ID = 1

WAGTAIL_SITE_NAME = 'Princeton Prosody Archive'

GRAPPELLI_ADMIN_TITLE = 'Princeton Prosody Archive Admin'

# username for logging activity by local scripts
SCRIPT_USERNAME = 'script'


# PUCAS configuration for CAS/LDAP login and user provisioning.
# Only includes non-sensitive configurations that do not change
PUCAS_LDAP = {
    # basic user profile attributes
    'ATTRIBUTES': ['givenName', 'sn', 'mail'],
    'ATTRIBUTE_MAP': {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    },
}

# django-csp configuration for content security policy definition and
# violation reporting - https://github.com/mozilla/django-csp

# fallback for all protocols: block it
CSP_DEFAULT_SRC = "'none'"

# allow loading js locally, from a cdn, and from google (for analytics)
CSP_SCRIPT_SRC = ("'self'", 'https://cdnjs.cloudflare.com',
                  'https://www.googletagmanager.com')

# allow loading fonts locally and from google (via data: url)
CSP_FONT_SRC = ("'self'", 'https://fonts.gstatic.com data:')

# allow loading css locally and from google (for fonts)
CSP_STYLE_SRC = ("'self'", 'https://fonts.googleapis.com')

# allow loading local images, hathi page images, google tracking pixel
CSP_IMG_SRC = ("'self'", 'https://babel.hathitrust.org',
               'https://www.google-analytics.com')

# exclude admin and cms urls from csp directives since they're authenticated
CSP_EXCLUDE_URL_PREFIXES = ('/admin', '/cms')

# allow usage of nonce for inline js (for analytics)
CSP_INCLUDE_NONCE_IN = ('script-src',)

# allow local scripts to connect to source (i.e. searchLoading)
CSP_CONNECT_SRC = ("'self'", "https://www.google-analytics.com")

##################
# LOCAL SETTINGS #
##################

# (local settings import logic adapted from mezzanine)

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local_settings import *", we use exec so that
# local_settings has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

f = os.path.join(BASE_DIR, "ppa", "local_settings.py")
if os.path.exists(f):
    import sys
    import imp
    module_name = "ppa.local_settings"
    module = imp.new_module(module_name)
    module.__file__ = f
    sys.modules[module_name] = module
    exec(open(f, "rb").read())

# Django webpack loader
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'static/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}


# if in debug mode and django-debug-toolbar is available, add to installed apps
if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    except ImportError:
        pass

    # allow webpack dev server through CSP when in DEBUG
    CSP_SCRIPT_SRC += ('http://localhost:3000', "'unsafe-eval'")
    CSP_STYLE_SRC += ('http://localhost:3000', "'unsafe-inline'")
    CSP_CONNECT_SRC += ('http://localhost:3000', 'ws://localhost:3000',)
