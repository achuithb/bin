#!/usr/bin/python

import argparse
import os
import shutil
import sys

import cros_paths
import git_lib
import utils


LINK = True
BASE_DIR = '/usr/local/google/home/achuith/code/'
CROS_DIR = os.path.join(BASE_DIR, 'cros/chromite')
CHROME_DIR = os.path.join(BASE_DIR, 'chrome/src/third_party/chromite')
CHROMITE = 'chromite'


def RemoveFile(filename):
  try:
    os.unlink(filename)
  except OSError:
    pass


def CreateLink(filename, copy):
  source = os.path.join(CROS_DIR, filename)
  dest = os.path.join(CHROME_DIR, filename)
  RemoveFile(dest)
  if copy:
    shutil.copyfile(source, dest)
  else:
    os.symlink(source, dest)
  git_lib.GitAddFile(dest)

def Create(copy):
  git_lib.AssertDetachedHead()
  git_lib.GitCreateBranch(CHROMITE)
  for filename in cros_paths.CHROMITE_FILES:
    CreateLink(filename, copy)
  git_lib.GitCommitWithMessage('Chromite debugging')


def Delete():
  git_lib.AssertOnBranch(CHROMITE)
  git_lib.GitCheckoutHEAD()
  git_lib.GitDeleteBranch(CHROMITE)


def Run(create, delete, copy):
  utils.AssertCWD(CHROME_DIR)
  if create and delete:
    raise Exception('Pick one of --create or --delete.')

  if not create and not delete:
    create = git_lib.DetachedHead()
    delete = not create

  if create:
    Create(copy)
  if delete:
    Delete()


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Setup chromite links in chrome source')
  parser.add_argument('--create', action='store_true', default=False,
                      help='create chromite links')
  parser.add_argument('--delete', action='store_true', default=False,
                      help='delete chromite links')
  parser.add_argument('--copy', action='store_true', default=False,
                      help='copy instead of linking')
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)
  Run(opts.create, opts.delete, opts.copy)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
