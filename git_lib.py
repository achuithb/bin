#!/usr/bin/python

import os
import subprocess

import utils

MASTER_BRANCH = 'master'


def GitBranch():
  return utils.RunCmd('git symbolic-ref --short HEAD').rstrip()


def GitListBranches():
  return utils.RunCmd('git branch --format=%(refname:short)').rstrip().split()


def GitCheckoutMaster():
  utils.RunCmd('git checkout %s' % MASTER_BRANCH)


def DetachedHead():
  return (utils.RunCmd('git status -sb').rstrip() == '## HEAD (no branch)')


def AssertOnBranch(branch=MASTER_BRANCH):
  if GitBranch() != branch:
    raise Exception('Not in expected branch %s.' % branch)


def AssertDetachedHead():
  if not DetachedHead():
    raise Exception('Not in detached head state.')


def GitSetUpstream(branch):
  utils.RunCmd('git branch --set-upstream-to=%s' % branch)


def GitRebaseMaster(branch):
  if branch == MASTER_BRANCH:
    return

  # This throws when rebase fails - handle this better.
  utils.RunCmd('git rebase master %s' % branch)


def GitCreateBranch(new_branch):
  utils.RunCmd('git checkout -b %s' % new_branch)


def GitDeleteBranch(branch):
  utils.RunCmd('git branch -D %s' % branch)


def GitCheckoutHEAD():
  utils.RunCmd('git checkout HEAD~')


def GitAddFile(filename):
  utils.RunCmd('git add %s' % filename)


def GitCommit():
  utils.RunCmd(['git', 'commit', '-a'], call=True)


def GitCommitWithMessage(commit_message):
  utils.RunCmd(['git', 'commit', '-a', '-m', commit_message])


def GitCommitFixup():
  utils.RunCmd('git commit -a --fixup=HEAD')


def GitAutoSquash():
  utils.RunCmd('git rebase -i --autosquash', call=True)


def GitUpload():
  utils.RunCmd('git cl upload', call=True)


def GitDiff():
  return utils.RunCmd('git diff')


def GitIsAhead():
  return utils.RunCmd('git status -sb').find('ahead') != -1


def GitNoCommit():
  return utils.RunCmd('git log --oneline --decorate -1').find(
      'origin/master') != -1


def GitPull():
  utils.AssertCWD([utils.CHROME_DIR, utils.CATAPULT_DIR])
  AssertOnBranch()
  utils.RunCmd('git pull')


def GitRebaseAll(skip_list = []):
  utils.AssertCWD([utils.CHROME_DIR, utils.CATAPULT_DIR])
  AssertOnBranch()
  for branch in GitListBranches():
    if branch not in skip_list:
      GitRebaseMaster(branch)
  GitCheckoutMaster()

