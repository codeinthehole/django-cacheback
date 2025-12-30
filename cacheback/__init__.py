import importlib.metadata as importlib_metadata


try:
    __version__ = importlib_metadata.version('django-cacheback')
except Exception:
    __version__ = 'HEAD'

default_app_config = 'cacheback.apps.CachebackConfig'
