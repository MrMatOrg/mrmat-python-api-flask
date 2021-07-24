#  MIT License
#
#  Copyright (c) 2021 MrMat
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import os
from setuptools import setup, find_packages

#
# Construct the version
# If we are running in the context of a GitHub action then we use the GITHUB_RUN_NUMBER
# otherwise we will default to 0 for the micro version.

major = os.environ['MAJOR'] if 'MAJOR' in os.environ else 0
minor = os.environ['MINOR'] if 'MINOR' in os.environ else 0
micro = os.environ['GITHUB_RUN_NUMBER'] if 'GITHUB_RUN_NUMBER' in os.environ else 0
dev = '.dev0' if 'IS_RELEASE' not in os.environ else ''

setup(
    name='mrmat-python-api-flask',
    version=f'{major}.{minor}.{micro}{dev}',
    packages=find_packages(),
    license='MIT',
    author='MrMat',
    author_email='imfeldma+9jqerw@gmail.com',
    description='Boilerplate for a Python Flask API',

    setup_requires=['flake8'],
    zip_safe=False,
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'mrmat-python-api-flask = mrmat_python_api_flask.cli:main',
            'mrmat-python-api-flask-client = mrmat_python_api_flask.client:main'
        ]
    }
)
