#!/usr/bin/python

import sys

import git_lib
import utils

def RepoRebase(skip_list=None, final_branch=None):
  if not skip_list:
    skip_list = []
  for branch in git_lib.GitListBranches():
    if branch not in skip_list:
      git_lib.GitCheckout(branch)
      utils.RunCmd('repo rebase .')
  if final_branch:
    git_lib.GitCheckout(final_branch)

def main(argv):
  RepoRebase(['old_refactor', 'qemu_version_retry'], 'unittest')

if __name__ == '__main__':
  sys.exit(main(sys.argv))
