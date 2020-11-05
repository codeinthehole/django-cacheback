try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    # This is required for Python versions < 3.8
    import importlib_metadata

try:
    __version__ = importlib_metadata.version('django-cacheback')
except Exception:
    __version__ = 'HEAD'

default_app_config = 'cacheback.apps.CachebackConfig'
