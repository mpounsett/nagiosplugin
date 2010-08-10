# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import glob
from setuptools import setup, find_packages


setup(
    name='nagiosplugin',
    version='0.3',
    description='Class library for Python Nagios plugins',
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'nagiosplugin': ['test/*.txt']},
    zip_safe=False,
    test_suite='nagiosplugin.test',
    data_files=[('doc', ['README.txt']),
                ('doc/examples', glob.glob('examples/*.py'))]
)
