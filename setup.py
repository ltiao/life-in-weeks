#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click',
    'python-dateutil'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='life_in_weeks',
    version='0.1.0',
    description="This is your life, and it's ending one week at a time.",
    long_description=readme + '\n\n' + history,
    author="Louis Tiao",
    author_email='louistiao@gmail.com',
    url='https://github.com/ltiao/life-in-weeks',
    packages=[
        'life_in_weeks',
    ],
    package_dir={'life_in_weeks':
                 'life_in_weeks'},
    entry_points={
        'console_scripts': [
            'life-in-weeks = life_in_weeks.main:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='life_in_weeks',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
