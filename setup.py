#!/usr/bin/env python

from setuptools import setup, find_packages
import os


setup(name='django-async-cache',
      version='0.1',
      url='https://github.com/codeinthehole/django-async-cache',
      author="David Winterbottom",
      author_email="david.winterbottom@gmail.com",
      description="Async cache objects that use Celery to refresh",
      long_description=os.path.join(os.path.dirname(__file__), 'README.rst'),
      license='MIT',
      packages=find_packages(exclude=["sandbox*", "tests*"]),
      include_package_data=True,
      install_requires=[
          'django==1.4',
          ],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Programming Language :: Python']
      )
