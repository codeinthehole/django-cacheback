from django.core import signals


def get_cache(backend, **kwargs):
    """
    Compatibilty wrapper for getting Django's cache backend instance

    original source: https://github.com/vstoykov/django-imagekit/commit/c26f8a0538778969a64ee471ce99b25a04865a8e
    """
    try:
        from django.core.cache import _create_cache
    except ImportError:
        # Django < 1.7
        from django.core.cache import get_cache as _get_cache
        return _get_cache(backend, **kwargs)

    cache = _create_cache(backend, **kwargs)
    # Some caches -- python-memcached in particular -- need to do a cleanup at the
    # end of a request cycle. If not implemented in a particular backend
    # cache.close is a no-op
    signals.request_finished.connect(cache.close)
    return cache
