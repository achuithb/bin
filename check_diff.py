#!/usr/bin/python

import os, sys

import utils


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
    'retry.py',
    'xbuddy.py',
    'xbuddy_unittest.py',
]

FILES = [
    'devserver_integration_test.py',
    'devserver.py',
    'health_checker.py',
    'autoupdate.py',
    'autoupdate_unittest.py',
    'cros_update_progress.py',
]

# android_build.py artifact_info.py build_artifact.py build_artifact_unittest.py build_util.py common_util.py common_util_unittest.py devserver_constants.py downloader.py downloader_unittest.py log_util.py retry.py xbuddy.py xbuddy_unittest.py

# devserver_integration_test.py devserver.py health_checker.py autoupdate.py autoupdate_unittest.py cros_update_progress.py

DIR1 = utils.AbsPath('code/cros/src/platform/dev/')
DIR2 = utils.AbsPath('code/cros/chromite/lib/xbuddy/')
DIR2 = utils.AbsPath('code/misc/xbuddy')

def main(argv):
  for f in FILES:
    path1 = os.path.join(DIR1, f)
    path2 = os.path.join(DIR2, f)
    try:
      utils.RunCmd(['/usr/bin/diff', path1, path2], silent=True)
    except Exception as e:
      utils.ColorPrint(utils.MAGENTA, f)
      print(e.output)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
