# -*- coding: utf-8 -*-
import codecs
import os

from distutils.util import convert_path
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
longdesc = []
for readme in ['README.txt', 'HACKING.txt', 'CONTRIBUTORS.txt', 'HISTORY.txt']:
    with codecs.open(readme, encoding='utf-8') as f:
        longdesc.append(f.read())

main_ns = {}
ver_path = convert_path('nagiosplugin/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='nagiosplugin',
    version=main_ns['__VERSION__'],
    description='Class library for writing Nagios (Icinga) plugins',
    long_description='\n\n'.join(longdesc),
    url='https://nagiosplugin.readthedocs.io/',
    download_url='https://pypi.org/project/nagiosplugin/',
    project_urls={
        'nagiosplugin source': 'https://github.com/mpounsett/nagiosplugin',
        'nagiosplugin issues':
        'https://github.com/mpounsett/nagiosplugin/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
    ],
    keywords='Nagios Icinga plugin check monitoring',
    author='Matthew Pounsett',
    author_email='matt@conundrum.com',
    license='ZPL-2.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
