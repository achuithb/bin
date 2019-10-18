#!/usr/bin/python

import os, sys

import utils


FILES = [
    '__init__.py',
    'nebraska.py',
    'nebraska_unittest.py',
    'README.md',
    'sample.json',
]

FILES = [
    'android_build.py',
    'artifact_info.py',
    'build_artifact.py',
    'build_util.py',
    'common_util.py',
    'devserver_constants.py',
    'downloader.py',
    'log_util.py',
    'retry.py',
    'xbuddy.py',
]

FILES = [
    'android_build.py',
    'artifact_info.py',
    'build_artifact.py',
    'build_artifact_unittest.py',
    'build_util.py',
    'common_util.py',
    'common_util_unittest.py',
    'devserver_constants.py',
    'downloader.py',
    'downloader_unittest.py',
    'log_util.py',
]


PLATFORM = 'src/platform/dev'
CHROMITE = 'chromite/lib'

def main(argv):
  for f in FILES:
    platform = os.path.join(utils.CROS_DIR, PLATFORM, f)
    chromite = os.path.join(utils.CROS_DIR, CHROMITE, f)
    try:
      utils.RunCmd(['/usr/bin/diff', platform, chromite], silent=True)
    except Exception as e:
      print(f)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
