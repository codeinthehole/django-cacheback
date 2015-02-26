#!/usr/bin/env python

from setuptools import setup, find_packages
import os
from cacheback import __version__

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(PACKAGE_DIR)


setup(name='django-cacheback',
      version=__version__,
      url='https://github.com/codeinthehole/django-cacheback',
      author="David Winterbottom",
      author_email="david.winterbottom@gmail.com",
      description=("Caching library for Django that uses Celery "
                   "to refresh cache items asynchronously"),
      long_description=open(os.path.join(PACKAGE_DIR, 'README.rst')).read(),
      license='MIT',
      packages=find_packages(exclude=["sandbox*", "tests*"]),
      include_package_data=True,
      install_requires=[
          'django>=1.3,<1.8',
          'django-celery>=3.0',
          'celery<3.2',
          'six',
          ],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Programming Language :: Python']
      )
