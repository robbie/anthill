#!/usr/bin/env python

from distutils.core import setup

setup(name='anthill',
      version='0.2.0-dev',
      description='Django apps for running a community website, developed for sunlightlabs.com',
      author='James Turk',
      author_email='jturk@sunlightfoundation.com',
      license='BSD',
      url='http://github.com/sunlightlabs/anthill/',
      packages=['anthill', 'anthill.events', 'anthill.events.templatetags',
                'anthill.people', 'anthill.people.templatetags',
                'anthill.projects', 'anthill.projects.templatetags'],
      package_data={'anthill.projects': ['templates/projects/*.html']},
)
