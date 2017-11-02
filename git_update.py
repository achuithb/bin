#!/usr/bin/python

import os, sys

import git_lib
import utils

def Pull():
  git_lib.GitPull()


def Rebase():
  git_lib.GitRebaseAll()


def Sync():
  if (os.getcwd() != utils.CHROME_DIR):
    return
  os.chdir(os.path.dirname(utils.CHROME_DIR))
  utils.RunCmd('gclient sync -j16')
  os.chdir(utils.CHROME_DIR)


def All():
  Pull()
  Sync()
  Rebase()


def main(argv):
  repo_map = { 'chrome' : utils.CHROME_DIR, 'catapult': utils.CATAPULT_DIR }
  func_map = { 'pull' : Pull, 'rebase' : Rebase, 'sync': Sync, 'all': All }

  if (len(argv) != 2 or
      argv[1] not in func_map.keys()):
    print 'Usage: %s [%s]' % (os.path.basename(argv[0]),
                              '|'.join(func_map.keys()))
    sys.exit(1)

  utils.AssertCWD([utils.CHROME_DIR, utils.CATAPULT_DIR])

  git_lib.GitCheckoutMaster()
  func_map[argv[1]]()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
