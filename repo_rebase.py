#!/usr/bin/python

import os, sys

import git_lib
import utils

def Rebase(dirs):
  if not dirs and utils.IsCrOS(root=True):
    print('Must specify directories to rebase.')
    sys.exit(1)

  if not dirs:
    dirs += ['.']
  cwd = os.getcwd()
  for d in dirs:
    print('Rebasing %s' % d)
    os.chdir(d)
    git_lib.GitRebaseAll()
    os.chdir(cwd)

def main(argv):
  dirs = argv[1:] if len(argv) else []
  Rebase(dirs)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
