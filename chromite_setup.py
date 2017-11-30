#!/usr/bin/python

import os
import shutil
import sys

import git_lib
import utils

# Run this script from ~/code/chrome/src/third_party/chromite/
# on master branch.

BASE_DIR = '/usr/local/google/home/achuith/code/'
CROS_DIR = os.path.join(BASE_DIR, 'cros/chromite')
CHROME_DIR = os.path.join(BASE_DIR, 'chrome/src/third_party/chromite')
MASTER_BRANCH = 'master'
VM_TEST_BRANCH = 'chromite'
DIRS = [
    'scripts',
    'cli/cros',
    'lib',
]


def CreateLink(dirname):
  print dirname
  source = os.path.join(CROS_DIR, dirname)
  link = os.path.join(CHROME_DIR, dirname)
  shutil.rmtree(link)
  os.symlink(source, link)
  git_lib.GitAddFile(link)


def Create():
  git_lib.AssertDetachedHead()
  git_lib.GitCreateBranch(MASTER_BRANCH)
  git_lib.GitCreateBranch(VM_TEST_BRANCH)
  for dirname in DIRS:
    CreateLink(dirname)
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

