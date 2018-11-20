#!/usr/bin/python

import os, sys

import git_lib
import utils

def Pull():
  git_lib.GitPull()


def Rebase():
  final_branch = None if utils.IsCrOS() else git_lib.MASTER_BRANCH
  git_lib.GitRebaseAll(final_branch=final_branch)


def Sync():
  if (os.getcwd() != utils.CHROME_DIR):
    return
  utils.GclientSync()

def All():
  Pull()
  Sync()
  Rebase()


def main(argv):
  repo_map = { 'chrome' : utils.CHROME_DIR, 'catapult': utils.CATAPULT_DIR }
  func_map = { 'pull' : Pull, 'rebase' : Rebase, 'sync': Sync, 'all': All }

  func = 'all'
  if (len(argv) == 2):
    func = argv[1]
    if func not in func_map.keys():
      print 'Unrecognized command %s\nUsage: %s [%s]' % (
          func, os.path.basename(argv[0]), '|'.join(func_map.keys()))
      sys.exit(1)

  # utils.AssertCWD([utils.CHROME_DIR, utils.CATAPULT_DIR])

  if not utils.IsCrOS():
    git_lib.GitCheckoutMaster()
  func_map[func]()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
