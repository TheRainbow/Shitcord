from setuptools import setup
import re

with open('README.md', 'r') as f:
    readme = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

with open('shitcord/__init__.py', 'r') as f:
    match = re.search(r'^__version__\s=\s\'(\d.\d.\d([ab])?)\'$', f.read(), re.MULTILINE)
    version = match.group(1)

# No extra requirements at the moment ¯\_(ツ)_/¯
extra_requires = {}

setup(
    name='Shitcord',
    version=version,
    author='Valentin B.',
    author_email='itisvale1@gmail.com',
    description='A framework to interact with the Discord API.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/itsVale/Shitcord',
    license='GNU General Public License v3 (GPLv3)',
    packages=['shitcord', 'shitcord.http', 'shitcord.gateway', 'shitcord.models', 'shitcord.events'],
    include_package_data=True,
    install_requires=requirements,
    extra_requires=extra_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
