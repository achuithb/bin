#!/usr/bin/python

import os, sys

import git_lib

def Prepare(path):
  os.chdir(path)
  git_lib.GitCheckoutMaster()


def Pull(path):
  git_lib.GitPull()


def Rebase(path):
  git_lib.GitRebaseAll()


def Sync(path):
  if (path != git_lib.CHROME_DIR):
    return
  os.chdir(os.path.dirname(git_lib.CHROME_DIR))
  git_lib.RunCmd('gclient sync -j16')


def All(path):
  Pull(path)
  Rebase(path)
  Sync(path)


def main(argv):
  repo_map = { 'chrome' : git_lib.CHROME_DIR, 'catapult': git_lib.CATAPULT_DIR }
  func_map = { 'pull' : Pull, 'rebase' : Rebase, 'sync': Sync, 'all': All }

  if (len(argv) != 3 or
      argv[1] not in repo_map.keys() or
      argv[2] not in func_map.keys()):
    func_str = '|'.join(func_map.keys())
    repo_str = '|'.join(repo_map.keys())
    print "Usage: %s [%s] [%s]" % (os.path.basename(argv[0]),
                                   repo_str, func_str)
    sys.exit(1)

  path = repo_map[argv[1]]
  Prepare(path)
  func_map[argv[2]](path)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
