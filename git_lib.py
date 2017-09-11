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


def AssertOnBranch(branch=MASTER_BRANCH):
  if GitBranch() != branch:
    raise Exception('Not in expected branch %s.' % branch)


def AssertCWD(path=CHROME_DIR):
  if os.path.commonprefix([path, os.getcwd()]) != path:
    raise Exception('Not at expected path %s' % path)


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

