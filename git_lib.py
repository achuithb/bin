#!/usr/bin/python

import os
import subprocess

CHROME_DIR = '/usr/local/google/home/achuith/code/chrome/src'
CATAPULT_DIR = '/usr/local/google/home/achuith/code/catapult'
MASTER_BRANCH = 'master'


def GitBranch():
  return subprocess.check_output(
    ['git', 'symbolic-ref', '--short', 'HEAD']).rstrip()


def GitListBranches():
  return subprocess.check_output(['git', 'branch',
                                  '--format=%(refname:short)']).rstrip().split()

def GitCheckoutMaster():
  subprocess.call(['git', 'checkout', MASTER_BRANCH])


def DetachedHead():
  return subprocess.check_output(
    ['git', 'status', '-sb']).rstrip() == '## HEAD (no branch)'


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

  print 'git rebase master %s' % branch
  # This throws when rebase fails - handle this better.
  print subprocess.check_output(['git', 'rebase', 'master', branch])


def GitCreateBranch(new_branch):
  subprocess.call(['git', 'checkout', '-b', new_branch])


def GitDeleteBranch(branch):
  subprocess.call(['git', 'branch', '-D', branch])


def GitCheckoutHEAD():
  subprocess.call(['git', 'checkout', 'HEAD~'])


def GitAddFile(filename):
  subprocess.call(['git', 'add', filename])


def GitCommit():
  print subprocess.call(['git', 'commit', '-a', '-m', 'chromite debugging'])


def GitRebaseAll(skip_list = []):
  AssertCWD([CHROME_DIR, CATAPULT_DIR])
  AssertOnBranch()
  for branch in GitListBranches():
    if branch not in skip_list:
      GitRebaseMaster(branch)
  GitCheckoutMaster()

