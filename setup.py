from setuptools import find_packages, setup

setup(
    name='db_migration',
    version='0.1',
    package_dir={'': 'db_migration'},
    packages=find_packages(where='db_migration')
)
