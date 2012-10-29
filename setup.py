# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
HISTORY = open(os.path.join(here, 'HISTORY.txt')).read()
HACKING = open(os.path.join(here, 'HACKING.txt')).read()
version = open(os.path.join(here, 'version.txt')).read().strip()


setup(
    name='nagiosplugin',
    version=version,
    description='Class library for writing Nagios (Icinga) plugins',
    long_description=README + '\n\n' + HISTORY + '\n\n' + HACKING,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
    ],
    keywords='Nagios Icinga plugin check monitoring',
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    url='http://projects.gocept.com/projects/nagiosplugin/wiki',
    download_url='http://pypi.python.org/pypi/nagiosplugin',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    test_suite='nagiosplugin.tests',
)
