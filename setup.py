# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages
import codecs
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
longdesc = []
for readme in ['README.txt', 'HACKING.txt', 'CONTRIBUTORS.txt', 'HISTORY.txt']:
    with codecs.open(readme, encoding='utf-8') as f:
        longdesc.append(f.read())
with codecs.open('version.txt', encoding='ascii') as f:
    version = f.read().strip()

if sys.version_info < (2, 7):
    extras_require = {'test': ['setuptools', 'unittest2', 'argparse']}
else:
    extras_require = {'test': ['setuptools']}


setup(
    name='nagiosplugin',
    version=version,
    description='Class library for writing Nagios (Icinga) plugins',
    long_description='\n\n'.join(longdesc),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
    ],
    keywords='Nagios Icinga plugin check monitoring',
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    url='http://projects.gocept.com/projects/nagiosplugin',
    download_url='http://pypi.python.org/pypi/nagiosplugin',
    license='ZPL-2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    test_suite='nagiosplugin.tests',
    extras_require=extras_require,
)
