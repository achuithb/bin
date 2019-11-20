#!/usr/bin/python

import os, sys

import git_lib
import utils


WIP = [
    os.path.join(utils.CROS_DIR, w) for w in [
        'chromite',
        'docs',
        'src/platform/dev',
        'src/third_party/chromiumos-overlay',
        'src/third_party/autotest/files',
    ]
]


def CheckoutMaster():
  if not utils.IsCrOS():
    return
  for wip in WIP:
    print(wip)
    os.chdir(wip)
    git_lib.GitCheckoutMaster()


def RepoRebase(dirs):
  AssertCWD(utils.CROS_DIR)
  if not dirs and IsCrOS(root=True):
    dirs = WIP
  if not dirs:
    dirs = ['.']

  cwd = os.getcwd()
  for d in dirs:
    utils.ColorPrint(BLUE, 'Rebasing %s' % d)
    os.chdir(d)
    git_lib.GitRebaseAll()
    git_lib.GitCheckoutMaster()
    utils.RunCmd('pyclean .')
    os.chdir(cwd)
