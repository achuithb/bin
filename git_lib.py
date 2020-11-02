#!/usr/bin/python

import subprocess

import utils

MASTER = 'master'
ORIGIN_MASTER = 'origin/master'
CHROMITE = 'chromite'


def GitBranch():
  return utils.RunCmd('git symbolic-ref --short HEAD').rstrip()


def IsBranchHead(branch):
  return (branch == MASTER or
          branch.find('HEAD detached at') != -1 or
          branch.find('no branch') != -1)


def GitListBranches():
  return utils.RunCmd(
      'git branch --format=%(refname:short)').rstrip().split('\n')


def GitCheckout(branch):
  utils.RunCmd('git checkout %s' % branch)


def GitCheckoutMaster():
  if MASTER in GitListBranches():
    GitCheckout(MASTER)


def GitDeleteMaster():
  AssertDetachedHead()
  if MASTER in GitListBranches():
    utils.RunCmd('git branch -d %s' % MASTER)


def GitCreateMaster():
  branches = GitListBranches()
  if MASTER in branches:
    GitCheckout(MASTER)
    return

  AssertDetachedHead()
  if len(branches) == 1:
    return
  if MASTER not in branches:
    GitCreateBranch(MASTER)


def DetachedHead():
  return (utils.RunCmd('git status -sb').rstrip() == '## HEAD (no branch)')


def AssertOnBranch(branch=MASTER):
  if GitBranch() != branch:
    raise Exception('Not in expected branch %s.' % branch)


def AssertDetachedHead():
  if not DetachedHead():
    raise Exception('Not in detached head state.')


def GitSetUpstream(branch):
  utils.RunCmd('git branch --set-upstream-to=%s' % branch)


def GitRebase(branch, unrebased, committed):
  if IsBranchHead(branch):
    return

  if utils.IsCrOS():
    rebase_cmd = 'repo rebase .'
    GitCheckout(branch)
  else:
    rebase_cmd = 'git rebase %s %s' % (MASTER, branch)

  try:
    utils.RunCmd(rebase_cmd)
  except subprocess.CalledProcessError:
    GitRebaseAbort()
    unrebased.append(branch)
  if not GitIsAhead() and branch != CHROMITE:
    committed.append(branch)


def GitCreateBranch(new_branch, commit=''):
  utils.RunCmd('git checkout -b %s %s' % (new_branch, commit))


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


def GitApply(diff_file):
  try:
    return utils.RunCmd(['git', 'apply', '--3way', diff_file])
  except subprocess.CalledProcessError as e:
    utils.ColorPrint(utils.RED, 'git apply failed : %r' % e)


def GitIsAhead():
  return utils.RunCmd('git status -sb').find('ahead') != -1


def GitNoCommit():
  return utils.RunCmd('git log --oneline --decorate -1').find(
      ORIGIN_MASTER) != -1


def GitPull():
  utils.AssertCWD([utils.CHROME_DIR, utils.CATAPULT_DIR])
  AssertOnBranch()
  utils.RunCmd('git pull', call=True)


def GitRebaseAll(skip_list=None):
  if not skip_list:
    skip_list = []
  if MASTER not in skip_list:
    skip_list.append(MASTER)
  unrebased = []
  committed = []
  branches = GitListBranches()
  for branch in branches:
    if branch.find('branch_') == 0 or branch in skip_list:
      utils.ColorPrint(utils.BLACK, 'Skipping %r' % branch)
    else:
      GitRebase(branch, unrebased, committed)
  if MASTER in branches:
    GitCheckout(MASTER)
  if unrebased:
    utils.ColorPrint(utils.RED, 'Unrebased branches: %r' % unrebased)
  if committed:
    utils.ColorPrint(utils.GREEN, 'Fully committed branches: %r' % committed)

def CheckoutRelease(branch, force):
  branch_name = 'branch_' + branch
  remote_branch = 'branch-heads/%s' % branch

  if branch_name in GitListBranches():
    if not force:
      raise Exception('branch %s exists; use --force to override.'
                      % branch_name)
    else:
      GitDeleteBranch(branch_name)
  GitCreateBranch(branch_name, remote_branch)
  GitSetUpstream(remote_branch)
