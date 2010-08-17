# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import glob
from setuptools import setup, find_packages


setup(
    name='nagiosplugin',
    version=file('version.txt').read().strip(),
    description='Class library for Python Nagios plugins',
    longdescription=file('README.txt').read(),
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'nagiosplugin': ['test/*.txt']},
    zip_safe=False,
    test_suite='nagiosplugin.test'
)
