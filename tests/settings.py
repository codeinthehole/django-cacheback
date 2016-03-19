SECRET_KEY = 'testing'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

INSTALLED_APPS = [
    # 'django.contrib.auth',
    # 'django.contrib.admin',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.sites',
    # 'django.contrib.flatpages',
    'cacheback',
    'tests.dummyapp',
]

BROKER_URL = 'django://'
CELERY_ALWAYS_EAGER = True

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
    }
}
