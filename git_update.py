#!/usr/bin/python

import sys

import git_lib
import utils

def Update():
  if not git_lib.GitDiff():
    print 'Diff empty, nothing to update'
    #return

  if not utils.IsCrOS() and git_lib.GitNoCommit():
    git_lib.GitCommit()
    return

  if not utils.IsCrOS():
    git_lib.GitCheckUpstream()
  git_lib.GitCommitFixup()
  git_lib.GitAutoSquash()


def main(argv):
  utils.AssertCWD([utils.CROS_DIR, utils.CHROME_DIR,
                   utils.CATAPULT_DIR, utils.BIN_DIR])
  Update();

if __name__ == '__main__':
  sys.exit(main(sys.argv))
