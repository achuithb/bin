#!/usr/bin/python

import subprocess
import sys

import git_lib
import utils

def RepoRebase(skip_list=None, final_branch=None):
  if not skip_list:
    skip_list = []
  unrebased = []
  committed = []
  for branch in git_lib.GitListBranches():
    if branch not in skip_list:
      git_lib.GitCheckout(branch)
      try:
        utils.RunCmd('repo rebase .')
      except subprocess.CalledProcessError:
        git_lib.GitRebaseAbort()
        unrebased.append(branch)
      if not git_lib.GitIsAhead():
        committed.append(branch)
  if final_branch:
    git_lib.GitCheckout(final_branch)
  if unrebased:
    print 'Unrebased branches: %r' % unrebased
  if committed:
    print 'Fully committed branches: %r' % committed

def main(argv):
  RepoRebase(['old_refactor'])

if __name__ == '__main__':
  sys.exit(main(sys.argv))
