import os
from setuptools import setup, find_packages

from cacheback import __version__


PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))


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
    'pytest',
    'pytest-cov',
    'pytest-flakes',
    'pytest-pep8',
    'pytest-django',
    'pytest-isort',
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
        'django>=1.5,<1.10',
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
