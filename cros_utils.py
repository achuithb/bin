#!/usr/bin/python

import os, sys

import cros_paths
import git_lib
import utils


CROS_MASTER = 'cros/master'
SCRIPTS_BASH_COMPLETION = 'bash_completion'


def _GetDirs(dirs=None):
  if dirs:
    return dirs
  if utils.IsCrOS(root=True):
    return cros_paths.WORKING_DIRS
  return ['.']


def CheckoutCrosMaster():
  utils.AssertCWD(utils.CROS_DIR)
  for wip in _GetDirs():
    utils.ColorPrint(utils.BLUE, wip)
    os.chdir(wip)
    if not git_lib.DetachedHead():
      git_lib.GitCheckout(CROS_MASTER)
    git_lib.GitDeleteMaster()
  os.chdir(utils.CROS_DIR)


def RepoRebase(dirs=None):
  utils.AssertCWD(utils.CROS_DIR)
  cwd = os.getcwd()
  for d in _GetDirs(dirs):
    utils.ColorPrint(utils.YELLOW, 'Rebasing %s' % d)
    os.chdir(d)
    git_lib.GitCreateMaster()
    git_lib.GitRebaseAll()
    utils.RunCmd('pyclean .')
    os.chdir(cwd)
