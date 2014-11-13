#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install as _install  
from setuptools.command.develop import develop as _develop
import sys, os, platform

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


THRUST_VERSION = 'v0.7.5'

version = '0.7.5'
install_requires = [
    'pyee'
]


ARCH = {                                                                        
    'cygwin': '32bit',                                                          
    'darwin': '64bit',                                                          
    'linux': platform.architecture()[0],                                       
    'win32': '32bit',                                                           
}[sys.platform]           

DIST_ARCH = {                                                                      
    '32bit': 'ia32',                                                               
    '64bit': 'x64',                                                                
}[ARCH]   
THRUST_PLATFORM = {
    'darwin': {
        'x64': 'darwin-x64'
    },
    'linux': {
        'ia32': 'linux-ia32',
        'x64': 'linux-x64',
    },
    'cygwin': {
      'ia32': 'win32-ia32'
    },
    'win32': {
      'ia32': 'win32-ia32'
    }
}[sys.platform][DIST_ARCH]
THRUST_BASE_URL = 'https://github.com/breach/thrust/releases/download/'


def _post_install():  
    import pythrust
    pythrust.download_binary(THRUST_BASE_URL, THRUST_VERSION, THRUST_PLATFORM)

class my_install(_install):  
    def run(self):
        _install.run(self)
        self.execute(_post_install, [],  msg="running post_install script")

class my_develop(_develop):  
    def run(self):
        self.execute(noop, (self.install_lib,), msg="Running develop task")
        _develop.run(self)
        self.execute(_post_install, [], msg="running post_develop script")


setup(name='pythrust',
    version=version,
    description="Python language bindings for Thrust",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='thrust application shell framework chromium content module python',
    author='Stanislas Polu',
    author_email='polu.stanislas@gmail.com',
    url='https://github.com/breach/pythrust',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    cmdclass={
        'install': my_install,  # override install
        'develop': my_develop   # develop is used for pip install -e .
    }  
)
