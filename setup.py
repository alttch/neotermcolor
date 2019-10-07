__version__ = '2.0.7'

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='neotermcolor',
    version=__version__,
    author='Altertech',
    author_email='div@altertech.com',
    description=
    'Fork of termcolor library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alttch/neotermcolor',
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing',
        'Topic :: Terminals'
    ),
)
