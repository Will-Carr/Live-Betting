"""live_betting python package configuration."""

from setuptools import setup

setup(
    name='live_betting',
    version='1.0.0',
    packages=['live_betting'],
    include_package_data=True,
    install_requires=[
        'flask',
        'bs4',
        'requests',
    ],
)
