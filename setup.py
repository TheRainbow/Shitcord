import re
from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    readme = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

with open('shitcord/__init__.py', 'r') as f:
    match = re.search(r'^__version__\s=\s\'(\d.\d.\d([ab])?)\'$', f.read(), re.MULTILINE)
    version = match.group(1)

extra_requires = {
    'performance': ['ujson>=1.35', 'erlastic>=2.0.0']
}

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
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extra_requires=extra_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
