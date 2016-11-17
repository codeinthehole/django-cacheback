import tempfile


SECRET_KEY = 'testing'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': tempfile.mkdtemp(),
    },
    'secondary': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': tempfile.mkdtemp(),
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

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
    }
}

CACHEBACK_TASK_QUEUE = 'rq'
