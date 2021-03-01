import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    lines = [line.strip() for line in f]
    requirements = [line for line in lines if line and not line.startswith('#')]

setup(
    name = 'qdii_value',
    version = '0.3.19',
    description = '计算 QDII 基金估值',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    url = 'https://github.com/xiaopc/qdii-value',
    author = 'xiaopc',
    author_email = 'i@xpc.im',
    license = 'MIT',
    packages = [
        'qdii_value',
        'qdii_value.cli',
        'qdii_value.provider',
        'qdii_value.provider.equity',
        'qdii_value.provider.fund',
    ],
    platforms = 'any',
    zip_safe = False,
    python_requires = '>=3.6',
    install_requires = requirements,
    entry_points = {
        'console_scripts': [
            'qdii-value=qdii_value.app:main'
        ]
    }
)