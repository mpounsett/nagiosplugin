# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages


setup(
    name='nagiosplugin',
    version='0.1dev',
    description='Class library for Python Nagios plugins',
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    test_suite='nagiosplugin.test'
)
