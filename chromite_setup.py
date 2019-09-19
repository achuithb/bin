#!/usr/bin/python

import os
import shutil
import sys

import git_lib
import utils

# Run this script from ~/code/chrome/src/third_party/chromite/
# on master branch.

LINK = True
BASE_DIR = '/usr/local/google/home/achuith/code/'
CROS_DIR = os.path.join(BASE_DIR, 'cros/chromite')
CHROME_DIR = os.path.join(BASE_DIR, 'chrome/src/third_party/chromite')
MASTER_BRANCH = 'master'
VM_TEST_BRANCH = 'chromite'
FILES = [
    'scripts/cros_run_vm_test.py',
    'scripts/cros_vm.py',
    'lib/cros_build_lib.py',
    'lib/path_util.py',
    'lib/gs.py',
    'cli/cros/cros_chrome_sdk.py',
    'cli/cros/cros_flash.py',
    'cli/flash.py',

    # Xbuddy.
    'lib/android_build.py',
    'lib/artifact_info.py',
    'lib/build_artifact.py',
    'lib/build_util.py',
    'lib/common_util.py',
    'lib/dev_server_wrapper.py',
    'lib/devserver_constants.py',
    'lib/downloader.py',
    'lib/log_util.py',
    'lib/retry.py',
    'lib/xbuddy.py',

    # Nebraska.
    'lib/auto_updater.py',
    'lib/nebraska_wrapper.py',
    'lib/nebraska.py',

    # 'lib/auto_updater.py',
    # 'lib/paygen/paygen_payload_lib.py',
    # 'scripts/deploy_chrome.py',
    # 'lib/constants.py',
    # 'lib/chrome_util.py',
    # 'lib/remote_access.py',
]


def RemoveFile(filename):
  try:
    os.unlink(filename)
  except OSError:
    pass


def CreateLink(filename):
  print filename
  source = os.path.join(CROS_DIR, filename)
  dest = os.path.join(CHROME_DIR, filename)
  RemoveFile(dest)
  if LINK:
    os.symlink(source, dest)
  else:
    shutil.copyfile(source, dest)
  git_lib.GitAddFile(dest)

def Create():
  git_lib.AssertDetachedHead()
  git_lib.GitCreateBranch(MASTER_BRANCH)
  git_lib.GitCreateBranch(VM_TEST_BRANCH)
  for filename in FILES:
    CreateLink(filename)
  git_lib.GitCommitWithMessage('Chromite debugging')

def Delete():
  git_lib.AssertOnBranch(VM_TEST_BRANCH)
  git_lib.GitCheckoutHEAD()
  git_lib.GitDeleteBranch(MASTER_BRANCH)
  git_lib.GitDeleteBranch(VM_TEST_BRANCH)


def Usage(argv):
  print 'Usage: %s [create|delete]' % argv[0].split('/')[-1]
  sys.exit(1)


def main(argv):
  utils.AssertCWD(CHROME_DIR)

  func_map = { 'create': Create, 'delete': Delete }
  if len(argv) != 2 or argv[1] not in func_map.keys():
    Usage(argv)
  func_map[argv[1]]()


if __name__ == '__main__':
  sys.exit(main(sys.argv))

