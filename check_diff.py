#!/usr/bin/python

import os, sys

import utils

FILES = ['android_build.py',
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

def main(argv):
  for f in FILES:
    plat = os.path.join('src/platform/dev', f)
    chromite = os.path.join('chromite/lib', f)
    try:
      utils.RunCmd(['/usr/bin/diff', plat, chromite], silent=True)
    except Exception as e:
      print 'diff %s %s' % (plat, chromite)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
