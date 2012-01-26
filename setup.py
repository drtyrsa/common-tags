#!/usr/bin/env python
# -*- coding:utf-8 -*-
from distutils.core import setup


setup(
    name = 'common-tags',
    version = '0.1.0',
    license = 'BSD',
    description = 'Common template tags for Django: forms rendering, messages rendering and so on',
    long_description = open('README.rst').read(),
    author = 'Vlad Starostin',
    author_email = 'drtyrsa@yandex.ru',
    packages = ['common_tags',
                'common_tags.templatetags',
                'common_tags.tests'],
    package_data={ 'common_tags': ['templates/common_tags/*'] },
    classifiers = [
        'Development Status :: 1 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)