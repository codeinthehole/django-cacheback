#!/usr/bin/env python

from setuptools import setup, find_packages
import os

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(PACKAGE_DIR)
print PACKAGE_DIR

setup(name='django-cacheback',
      version='0.1',
      url='https://github.com/codeinthehole/django-cacheback',
      author="David Winterbottom",
      author_email="david.winterbottom@gmail.com",
      description="Caching library for Django that uses Celery to refresh cache items asynchronously",
      long_description=os.path.join(PACKAGE_DIR, 'README.rst'),
      license='MIT',
      packages=find_packages(exclude=["sandbox*", "tests*"]),
      include_package_data=True,
      install_requires=[
          'django>=1.3',
          ],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Programming Language :: Python']
      )
