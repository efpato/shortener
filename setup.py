# -*- coding: utf-8 -*-

import pathlib
from setuptools import find_packages, setup


def read_version():
    filename = pathlib.Path(__file__).parent / 'VERSION'
    with open(filename) as f:
        return f.read().strip()


setup(
    name='shortener',
    version=read_version(),
    description='URL shortener',
    author="Sergey Demenok",
    author_email="sergey.demenok@gmail.ru",
    platforms=['POSIX'],
    packages=find_packages(),
    install_requires=[
        'aiodns~=1.2.0',
        'aiohttp~=3.5.4',
        'aiohttp-basicauth-middleware~=1.1.0',
        'PyYAML~=4.2b1',
        'aiotarantool @ git+https://github.com/shveenkov/aiotarantool.git',
    ]
)
