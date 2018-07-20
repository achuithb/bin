#!/usr/bin/python

import os
import subprocess

import utils

MASTER_BRANCH = 'master'


def GitBranch():
  return utils.RunCmd('git symbolic-ref --short HEAD').rstrip()


def GitListBranches():
  return utils.RunCmd('git branch --format=%(refname:short)').rstrip().split()


def GitCheckout(branch):
  utils.RunCmd('git checkout %s' % branch)


def GitCheckoutMaster():
  GitCheckout(MASTER_BRANCH)


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
  try:
    utils.RunCmd('git rebase master %s' % branch)
  except subprocess.CalledProcessError as e:
    print('rebase of branch %s failed' % branch)
    if not RebaseFunctionHistogram():
      raise e

def RebaseFunctionHistogram():
  return False
  histogram_file = 'extensions/browser/extension_function_histogram_value.h'
  skip_lines = ['<<<<<<< HEAD', '=======', '>>>>>>>']

  diff = GitDiff().split('\n')
  if not diff or diff[0] != ('diff --cc %s' % histogram_file):
    return False
  content = ''
  with open(histogram_file, 'r') as f:
    for line in f:
      for s in skip_lines:
        if line and len(line) >= len(s) and line[0:len(s)] == s:
           line = None
      if line is not None:
        content += line
  open(histogram_file, 'w').write(content)

  GitAddFile(histogram_file)
  GitRebaseContinue()
  return True


def GitCreateBranch(new_branch):
  utils.RunCmd('git checkout -b %s' % new_branch)


def GitDeleteBranch(branch):
  utils.RunCmd('git branch -D %s' % branch)


def GitCheckoutHEAD():
  GitCheckout('HEAD~')


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


def GitRebaseContinue():
  utils.RunCmd('git rebase --continue')


def GitRebaseAbort():
  utils.RunCmd('git rebase --abort')


def GitUpload(presubmit):
  cmd = ['git', 'cl', 'upload']
  if not presubmit:
    cmd += ['--bypass-hooks']
  utils.RunCmd(cmd, call=True)


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
  utils.RunCmd('git pull', call=True)


def GitRebaseAll(skip_list=None):
  if not skip_list:
    skip_list = []
  utils.AssertCWD([utils.CHROME_DIR, utils.CATAPULT_DIR])
  AssertOnBranch()
  for branch in GitListBranches():
    if branch not in skip_list:
      GitRebaseMaster(branch)
  GitCheckoutMaster()

