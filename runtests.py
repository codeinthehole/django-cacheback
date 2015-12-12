#!/usr/bin/env python
import sys
from optparse import OptionParser

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        CACHES={
            'default': {
                'BACKEND':
                'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake'
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.flatpages',
            'cacheback',
            'tests.dummyapp',
            ],
        BROKER_URL = 'django://',
        CELERY_ALWAYS_EAGER=True,
        NOSE_ARGS=['-s', '--with-spec'],
    )

from django_nose import NoseTestSuiteRunner


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    test_runner = NoseTestSuiteRunner(verbosity=1)
    num_failures = test_runner.run_tests(test_args)
    if num_failures > 0:
        sys.exit(num_failures)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
