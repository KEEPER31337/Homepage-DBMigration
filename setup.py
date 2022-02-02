from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup

setup(
    name='typedef',
    version='0.1',
    packages=find_packages(where='shared'),
    package_dir={'': 'shared'},
    py_modules=[splitext(basename(path))[0] for path in glob('shared/*.py')],
)

setup(
    name='db_migration',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
)
