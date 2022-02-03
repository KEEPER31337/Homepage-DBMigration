from setuptools import find_packages, setup

setup(
    name='db_migration',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src')
)
