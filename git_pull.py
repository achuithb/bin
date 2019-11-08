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


def CrOSCheckoutMaster():
  for wip in WIP:
    print(wip)
    os.chdir(wip)
    git_lib.GitCheckoutMaster()


def Pull():
  if utils.IsCrOS():
    utils.RunCmd('repo sync', call=True)
  else:
    git_lib.GitPull()


def Rebase():
  if utils.IsCrOS():
    utils.RepoRebase(WIP)
  else:
    git_lib.GitRebaseAll(final_branch=git_lib.MASTER_BRANCH)


def Sync():
  utils.GclientSync()


def All():
  Pull()
  Sync()
  Rebase()


def main(argv):
  repo_map = { 'chrome' : utils.CHROME_DIR, 'catapult': utils.CATAPULT_DIR }
  func_map = { 'pull' : Pull, 'rebase' : Rebase, 'sync': Sync, 'all': All }

  func = 'all'
  if (len(argv) == 2):
    func = argv[1]
    if func not in func_map.keys():
      print 'Unrecognized command %s\nUsage: %s [%s]' % (
          func, os.path.basename(argv[0]), '|'.join(func_map.keys()))
      sys.exit(1)

  if utils.IsCrOS():
    CrOSCheckoutMaster()
  else:
    git_lib.GitCheckoutMaster()

  func_map[func]()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
