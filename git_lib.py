#!/usr/bin/python

import os
import subprocess

CHROME_DIR = '/usr/local/google/home/achuith/code/chrome/src'
CATAPULT_DIR = '/usr/local/google/home/achuith/code/catapult'
MASTER_BRANCH = 'master'

def RunCmd(args):
  if isinstance(args, str):
    args = args.split()
  if not isinstance(args, list):
    raise Exception('RunCmd: malformed cmd %r' % args)

  print 'RunCmd: %s' % (' ').join(args)
  ret = subprocess.check_output(args)
  print 'RunCmd response:\n%s' % ret
  return ret


def GitBranch():
  return RunCmd('git symbolic-ref --short HEAD').rstrip()


def GitListBranches():
  return RunCmd('git branch --format=%(refname:short)').rstrip().split()


def GitCheckoutMaster():
  RunCmd('git checkout %s' % MASTER_BRANCH)


def DetachedHead():
  return (RunCmd('git status -sb').rstrip() == '## HEAD (no branch)')


def AssertOnBranch(branch=MASTER_BRANCH):
  if GitBranch() != branch:
    raise Exception('Not in expected branch %s.' % branch)


def AssertCWD(paths):
  if isinstance(paths, str):
    paths = [paths]
  if not isinstance(paths, list):
    raise Exception('%s should be an array of paths' % paths)

  for path in paths:
    if os.path.commonprefix([path, os.getcwd()]) == path:
      return
  raise Exception('Not at expected path(s) %r' % paths)


def AssertDetachedHead():
  if not DetachedHead():
    raise Exception('Not in detached head state.')


def GitRebaseMaster(branch):
  if branch == MASTER_BRANCH:
    return

  # This throws when rebase fails - handle this better.
  RunCmd('git rebase master %s' % branch)


def GitCreateBranch(new_branch):
  RunCmd('git checkout -b %s' % new_branch)


def GitDeleteBranch(branch):
  RunCmd('git branch -D %s' % branch)


def GitCheckoutHEAD():
  RunCmd('git checkout HEAD~')


def GitAddFile(filename):
  RunCmd('git add %s' % filename)


def GitCommit(commit_message):
  RunCmd(['git', 'commit', '-a', '-m', commit_message])


def GitPull():
  AssertCWD([CHROME_DIR, CATAPULT_DIR])
  AssertOnBranch()
  RunCmd('git pull')


def GitRebaseAll(skip_list = []):
  AssertCWD([CHROME_DIR, CATAPULT_DIR])
  AssertOnBranch()
  for branch in GitListBranches():
    if branch not in skip_list:
      GitRebaseMaster(branch)
  GitCheckoutMaster()

