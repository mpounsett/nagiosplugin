# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import glob
from setuptools import setup, find_packages


setup(
    name='nagiosplugin',
    version=file('version.txt').read().strip(),
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    url='http://projects.gocept.com/projects/projects/nagiosplugin/wiki',
    description='Class library for writing Nagios/Icinga plugins',
    long_description=file('README.txt').read(),
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
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'nagiosplugin': ['test/*.txt']},
    zip_safe=False,
    test_suite='nagiosplugin.test',
    setup_requires=['setuptools_hg']
)
