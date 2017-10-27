#!/usr/bin/python

import os, sys

import git_lib

def Pull():
  git_lib.GitPull()


def Rebase():
  git_lib.GitRebaseAll()


def Sync():
  if (os.getcwd() != git_lib.CHROME_DIR):
    return
  os.chdir(os.path.dirname(git_lib.CHROME_DIR))
  git_lib.RunCmd('gclient sync -j16')
  os.chdir(git_lib.CHROME_DIR)


def All():
  Pull()
  Sync()
  Rebase()


def main(argv):
  repo_map = { 'chrome' : git_lib.CHROME_DIR, 'catapult': git_lib.CATAPULT_DIR }
  func_map = { 'pull' : Pull, 'rebase' : Rebase, 'sync': Sync, 'all': All }

  if (len(argv) != 2 or
      argv[1] not in func_map.keys()):
    print 'Usage: %s [%s]' % (os.path.basename(argv[0]),
                              '|'.join(func_map.keys()))
    sys.exit(1)

  if (os.getcwd() not in [git_lib.CHROME_DIR, git_lib.CATAPULT_DIR]):
    print '%s is not a valid cwd for this command' % os.getcwd()
    sys.exit(1)

  git_lib.GitCheckoutMaster()
  func_map[argv[1]]()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
