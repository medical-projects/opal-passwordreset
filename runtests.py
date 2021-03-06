"""
Standalone test runner for passwordreset plugin
"""
import os
import sys
from django.conf import settings

settings.configure(DEBUG=True,
                   DATABASES={
                       'default': {
                           'ENGINE': 'django.db.backends.sqlite3',
                       }
                   },
                   ROOT_URLCONF='opal.urls',
                   STATIC_URL='/assets/',
                   COMPRESS_ROOT=os.path.join(os.sep, 'tmp'),
                   DATE_FORMAT='d/m/Y',
                   DATE_INPUT_FORMATS=['%d/%m/%Y'],
                   DATETIME_FORMAT='d/m/Y H:i:s',
                   DATETIME_INPUT_FORMATS=['%d/%m/%Y %H:%M:%S'],
                   TIME_FORMAT="H:i:s",
                   MIDDLEWARE=(
                       'django.middleware.common.CommonMiddleware',
                       'django.contrib.sessions.middleware.SessionMiddleware',
                       'opal.middleware.AngularCSRFRename',
                       'django.middleware.csrf.CsrfViewMiddleware',
                       'django.contrib.auth.middleware.AuthenticationMiddleware',
                       'django.contrib.messages.middleware.MessageMiddleware',
                       'opal.middleware.DjangoReversionWorkaround',
                       'reversion.middleware.RevisionMiddleware',
                   ),
                   TEMPLATES=[
                        {
                            'BACKEND': 'django.template.backends.django.DjangoTemplates',
                            'DIRS': [
                                os.path.join(".", 'templates'),
                            ],
                            'APP_DIRS': True,
                            'OPTIONS': {
                                'context_processors': [
                                    'django.contrib.auth.context_processors.auth',
                                    'django.template.context_processors.debug',
                                    'django.template.context_processors.i18n',
                                    'django.template.context_processors.media',
                                    'django.template.context_processors.static',
                                    'django.template.context_processors.tz',
                                    'django.template.context_processors.request',
                                ],
                            },
                        },
                   ],
                   OPAL_BRAND_NAME='OPAL_BRAND',
                   INSTALLED_APPS=('django.contrib.auth',
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   'django.contrib.staticfiles',
                                   'django.contrib.admin',
                                   'compressor',
                                   'opal',
                                   'passwordreset',))

import django
django.setup()

from opal.core import application

class Application(application.OpalApplication):
    pass

try:
    sys.argv.remove('--failfast')
    failfast = True
except ValueError:
    failfast = False


from django.test.runner import DiscoverRunner
test_runner = DiscoverRunner(verbosity=1, failfast=failfast)
if len(sys.argv) == 2:
    failures = test_runner.run_tests([sys.argv[-1], ])
else:
    failures = test_runner.run_tests(['passwordreset', ])
if failures:
    sys.exit(failures)