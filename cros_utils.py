#!/usr/bin/python

import os, sys

import cros_paths
import git_lib
import utils


def _GetDirs(dirs):
  if dirs:
    return dirs
  if utils.IsCrOS(root=True):
    return cros_paths.WORKING_DIRS
  return ['.']


def CheckoutMaster(dirs=None):
  utils.AssertCWD(utils.CROS_DIR)
  for wip in _GetDirs(dirs):
    print(wip)
    os.chdir(wip)
    git_lib.GitCheckoutMaster()
  os.chdir(utils.CROS_DIR)


def RepoRebase(dirs=None):
  utils.AssertCWD(utils.CROS_DIR)
  cwd = os.getcwd()
  for d in _GetDirs(dirs):
    utils.ColorPrint(utils.BLUE, 'Rebasing %s' % d)
    os.chdir(d)
    git_lib.GitRebaseAll()
    git_lib.GitCheckoutMaster()
    utils.RunCmd('pyclean .')
    os.chdir(cwd)
