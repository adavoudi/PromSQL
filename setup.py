from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'promsql', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='promsql',
    version=version['__version__'],
    description=('PromQL on top of SQL and Pandas'),
    long_description=long_description,
    author='Alireza Davoudi',
    author_email='davoudialireza+promsql@gmail.com',
    url='https://github.com/adavoudi/PromSQL',
    license='',
    packages=['promsql'],
#   install_requires=[
#       'dependency==1.2.3',
#   ],
    scripts=['bin/promsql-cli.py'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7'],
    )
