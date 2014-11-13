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
                os.chmod(thrust_shell_path, st.st_mode | stat.S_IEXEC)

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

