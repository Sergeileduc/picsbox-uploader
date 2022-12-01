#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# requirements = ['Click>=7.0', ]
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

test_requirements = []

setup(
    author="Sergeileduc",
    author_email='sergei.leduc@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Upload to picsbox",
    entry_points={
        'console_scripts': [
            'picsbox-up=picsbox_uploader.cli:app',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='picsbox_uploader',
    name='picsbox_uploader',
    packages=find_packages(include=['picsbox_uploader', 'picsbox_uploader.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Sergeileduc/picsbox_uploader',
    version='0.1.0',
    zip_safe=False,
)
