#!/usr/bin/python

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


def _GitRebaseMaster(branch, unrebased, committed):
  if branch == MASTER_BRANCH:
    return

  if utils.IsCrOS():
    rebase_cmd = 'repo rebase .'
    GitCheckout(branch)
  else:
    rebase_cmd = 'git rebase master %s' % branch

  try:
    utils.RunCmd(rebase_cmd)
  except subprocess.CalledProcessError:
    GitRebaseAbort()
    unrebased.append(branch)
  if not GitIsAhead():
    committed.append(branch)


def GitCreateBranch(new_branch, commit=None):
  cmd = 'git checkout -b %s' % new_branch
  if commit:
    cmd += ' ' + commit
  utils.RunCmd(cmd)


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
  if utils.IsCrOS():
    utils.RunCmd('repo sync', call=True)
  else:
    utils.AssertCWD([utils.CHROME_DIR, utils.CATAPULT_DIR])
    AssertOnBranch()
    utils.RunCmd('git pull', call=True)


def GitRebaseAll(skip_list=None, final_branch=None):
  if not skip_list:
    skip_list = []
  unrebased = []
  committed = []
  # utils.AssertCWD([utils.CHROME_DIR, utils.CATAPULT_DIR])
  # AssertOnBranch()
  for branch in GitListBranches():
    if branch not in skip_list:
      _GitRebaseMaster(branch, unrebased, committed)
  if final_branch:
    GitCheckout(final_branch)
  if unrebased:
    print 'Unrebased branches: %r' % unrebased
  if committed:
    print 'Fully committed branches: %r' % committed


