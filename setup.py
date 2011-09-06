try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='appy',
    version='0.9.0',
    description='A framework for python application development. Provides cli, logging, \
                threading facilities.',
    author='Sreejith K / K7Computing Pvt Ltd',
    author_email='sreejithemk@gmail.com',
    url='http://www.foobarnbaz.com',
    install_requires=[
    ],
    setup_requires=[],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=True,
)
