import os
from setuptools import setup, find_packages

from cacheback import __version__


PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))


# TEMPORARY FIX FOR
# https://bitbucket.org/pypa/setuptools/issues/450/egg_info-command-is-very-slow-if-there-are
TO_OMIT = ['.git', '.tox']
orig_os_walk = os.walk
def patched_os_walk(path, *args, **kwargs):
    for (dirpath, dirnames, filenames) in orig_os_walk(path, *args, **kwargs):
        if '.git' in dirnames:
            # We're probably in our own root directory.
            print("MONKEY PATCH: omitting a few directories like .git and .tox...")
            dirnames[:] = list(set(dirnames) - set(TO_OMIT))
        yield (dirpath, dirnames, filenames)

os.walk = patched_os_walk
# END IF TEMPORARY FIX.


celery_requirements = [
    'celery',
]

rq_requirements = [
    'django-rq>=0.9',
]

test_requirements = [
    'tox',
    'tox-pyenv',
    'mock',
    'freezegun>=0.3.7',
    'pytest>=3.0.3',
    'pytest-cov>=2.4.0',
    'pytest-flakes>=1.0.1',
    'pytest-pep8>=1.0.6',
    'pytest-django>=3.0.0',
    'pytest-isort>=0.1.0',
] + celery_requirements + rq_requirements


setup(
    name='django-cacheback',
    version=__version__,
    url='https://github.com/codeinthehole/django-cacheback',
    author="David Winterbottom",
    author_email='david.winterbottom@gmail.com',
    description=(
        'Caching library for Django that uses Celery or '
        'RQ to refresh cache items asynchronously'
    ),
    long_description=open(os.path.join(PACKAGE_DIR, 'README.rst')).read(),
    license='MIT',
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    include_package_data=True,
    install_requires=[
        'django>=1.8,<2.0',
    ],
    extras_require={
        'celery': celery_requirements,
        'rq': rq_requirements,
        'tests': test_requirements,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
