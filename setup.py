# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()
version = open(os.path.join(here, 'version.txt')).read().strip()


setup(
    name='nagiosplugin',
    version=file('version.txt').read().strip(),
    description='Class library for writing Nagios/Icinga plugins',
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
    ],
    keywords='Nagios Icinga plugin check monitoring',
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    url='http://projects.gocept.com/projects/projects/nagiosplugin/wiki',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data = {'': ['*.txt', '*.rst']},
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    test_suite='nagiosplugin.test'
)
