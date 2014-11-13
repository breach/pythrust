import urllib
import contextlib
import zipfile
import tempfile
import errno
import os
import inspect
import sys
import shutil

def download_and_extract(destination, url):
    print(url)
    with tempfile.TemporaryFile() as t:
        with contextlib.closing(urllib.request.urlopen(url)) as u:
            while True:
                chunk = u.read(1024*1024)
                if not len(chunk):
                    break
                sys.stderr.write('.')
                sys.stderr.flush()
                t.write(chunk)
        sys.stderr.write('\nExtracting...\n')
        sys.stderr.flush()
        with zipfile.ZipFile(t) as z:
            z.extractall(destination)

def rm_rf(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def boostrap(base_url, version, platform, force=False):
    SOURCE_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(
      inspect.currentframe())))
    THRUST_PATH = os.path.join(SOURCE_ROOT, '..', 'vendor', 'thrust')
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
            sys.stderr.write('Found {0}n'.format(version))
            return

    rm_rf(THRUST_PATH)

    sys.stderr.write('Downloading {0}...\n'.format(THRUST_RELEASE_URL))
    sys.stderr.flush()
    download_and_extract(THRUST_PATH, THRUST_RELEASE_URL)
    with open(THRUST_VERSION_PATH, 'w') as f:
        f.write('{0}\n'.format(THRUST_RELEASE_URL))

