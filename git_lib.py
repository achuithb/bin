#!/usr/bin/python

import os
import subprocess

CHROME_DIR = '/usr/local/google/home/achuith/code/chrome/src'
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


def AssertCWD(path=CHROME_DIR):
  if os.path.commonprefix([path, os.getcwd()]) != path:
    raise Exception('Not at expected path %s' % path)


def AssertDetachedHead():
  if not DetachedHead():
    raise Exception('Not in detached head state.')


def GitRebaseMaster(branch):
  if branch == MASTER_BRANCH:
    return

  print 'git rebase master %s' % branch
  return
  print subprocess.check_output(['git', 'rebase', 'master', branch])


def GitRebaseAll():
  AssertCWD()
  AssertOnBranch()
  for branch in GitListBranches():
    GitRebaseMaster(branch)
  GitCheckoutMaster()


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

