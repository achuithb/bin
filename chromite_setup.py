#!/usr/bin/python

import argparse
import os
import shutil
import sys

import cros_paths
import git_lib
import utils


# Run this script from ~/code/chrome/src/third_party/chromite/
# on master branch.

LINK = True
BASE_DIR = '/usr/local/google/home/achuith/code/'
CROS_DIR = os.path.join(BASE_DIR, 'cros/chromite')
CHROME_DIR = os.path.join(BASE_DIR, 'chrome/src/third_party/chromite')
MASTER_BRANCH = 'head'
VM_TEST_BRANCH = 'chromite'


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
  for filename in cros_paths.CHROMITE_FILES:
    CreateLink(filename)
  git_lib.GitCommitWithMessage('Chromite debugging')

def Delete():
  git_lib.AssertOnBranch(VM_TEST_BRANCH)
  git_lib.GitCheckoutHEAD()
  git_lib.GitDeleteBranch(MASTER_BRANCH)
  git_lib.GitDeleteBranch(VM_TEST_BRANCH)


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Setup chromite links in chrome source')
  parser.add_argument('--create', action='store_true', default=False,
                      help='create chromite links')
  parser.add_argument('--delete', action='store_true', default=False,
                      help='delete chromite links')
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)
  utils.AssertCWD(CHROME_DIR)

  if rem:
    raise Exception('Unknown args: %s' % rem)
  if ((opts.create and opts.delete) or
      (not opts.create and not opts.delete)):
    raise Exception('Pick one of --create or --delete.')

  if opts.create:
    Create()
  if opts.delete:
    Delete()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
