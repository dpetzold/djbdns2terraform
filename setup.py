#!/usr/bin/env python

from setuptools import setup

setup(
    name='djbdns2terraform',
    version='0.0.1',
    description='Create Route53 resource records from a djbdns file',
    author='Derrick Petzold',
    author_email='github@bzero.io',
    url='https://github.com/dpetzold/djbdns2terraform',
    setup_requires=[
        'pytest-runner',
    ],
    tests_requires=[
        'pytest',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Text Processing"
    ],
    entry_points={
        'console_scripts': [
            'djbdns2terraform = djbdns2terraform.main:main'
        ]
    },
)
