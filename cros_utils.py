#!/usr/bin/python

import os, sys

import git_lib
import utils


WIP = [
    os.path.join(utils.CROS_DIR, w) for w in [
        'chromite',
        'docs',
        'src/platform/dev',
        'src/platform2',
        'src/private-overlays/overlay-amd64-generic-cheets-private',
        'src/private-overlays/overlay-betty-private',
        'src/third_party/chromiumos-overlay',
        'src/third_party/autotest/files',
        'src/third_party/autotest-private',
    ]
]


def _GetDirs(dirs):
  if dirs:
    return dirs
  if utils.IsCrOS(root=True):
    return WIP
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
