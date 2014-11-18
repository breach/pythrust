#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install as _install  
from setuptools.command.develop import develop as _develop

import urllib
import contextlib
import zipfile
import tempfile
import errno
import os
import inspect
import sys
import shutil
import stat
import subprocess
import platform

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

def execute(argv):
  try:
    output = subprocess.check_output(argv)
    return output
  except subprocess.CalledProcessError as e:
    print(e.output)
    raise e


def download_and_extract(destination, url):
    with tempfile.NamedTemporaryFile() as t:
        with contextlib.closing(urllib.request.urlopen(url)) as u:
            while True:
                chunk = u.read(1024*1024)
                if not len(chunk):
                    break
                sys.stderr.write('.')
                sys.stderr.flush()
                t.write(chunk)
        sys.stderr.write('\nExtracting to {0}\n'.format(destination))
        sys.stderr.flush()
        if sys.platform == 'darwin':
            # Use unzip command on Mac to keep symbol links in zip file work.
            execute(['unzip', str(t.name), '-d', destination])
        else:
            with zipfile.ZipFile(t) as z:
                z.extractall(destination)
            if sys.platform == 'linux':
                thrust_shell_path = os.path.join(destination, 'thrust_shell');
                st = os.stat(thrust_shell_path)
                os.chmod(thrust_shell_path, 
                         st.st_mode | 
                         stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def rm_rf(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def boostrap(dest, base_url, version, platform, force=False):
    THRUST_PATH = os.path.realpath(
        os.path.join(dest, 'vendor', 'thrust'))
    THRUST_VERSION_PATH = os.path.join(THRUST_PATH, '.version')
    THRUST_RELEASE_FILENAME = 'thrust-' + version + '-' + platform + '.zip'
    THRUST_RELEASE_URL = base_url + version + '/' + THRUST_RELEASE_FILENAME;

    if force is False:
        existing_version = ''
        try:
            with open(THRUST_VERSION_PATH, 'r') as f:
                existing_version = f.readline().strip()
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
        if existing_version == THRUST_RELEASE_URL:
            sys.stderr.write('Found {0} at {1}\n'.format(version, THRUST_PATH))
            sys.stderr.flush()
            return

    rm_rf(THRUST_PATH)
    os.makedirs(THRUST_PATH)

    sys.stderr.write('Downloading {0}...\n'.format(THRUST_RELEASE_URL))
    sys.stderr.flush()
    download_and_extract(THRUST_PATH, THRUST_RELEASE_URL)
    with open(THRUST_VERSION_PATH, 'w') as f:
        f.write('{0}\n'.format(THRUST_RELEASE_URL))



def _post_install(dest):  
    boostrap(dest, 
            THRUST_BASE_URL, THRUST_VERSION, THRUST_PLATFORM)

class my_install(_install):  
    def run(self):
        _install.run(self)
        self.execute(_post_install, 
                [os.path.join(self.install_platlib, self.config_vars['dist_name'])],  
                msg="running post_install script")

class my_develop(_develop):  
    def run(self):
        _develop.run(self)
        self.execute(_post_install, 
                [os.path.join(self.install_platlib, self.config_vars['dist_name'])],  
                msg="running post_develop script")


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
