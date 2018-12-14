"""live-betting python package configuration."""

from setuptools import setup

setup(
    name='live-betting',
    version='1.0.0',
    packages=['live-betting'],
    include_package_data=True,
    install_requires=[
        'flask',
        'nodeenv',
        'sh',
        'Flask-Testing',
        'selenium',
        'requests',
        'arrow'
    ],
)
