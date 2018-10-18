#!/usr/bin/python

import os, sys

import git_lib
import utils

COMMIT_FILE = 'commit.txt'

def CreateBranch(index):
  # open commit file.
  with open(COMMIT_FILE) as f:
    lines = f.read().splitlines()
  # format: commit <hash>
  _, commit = lines[index].split()

  git_lib.GitCreateBranch('bisect_%d' % index, commit)
  utils.GclientSync()


def RunTest():
  utils.RunCmd(
      'cros_run_vm_test --build --deploy --build-dir=out_amd64-generic/Release '
      '--cmd -- /usr/local/autotest/bin/autotest '
      '/usr/local/autotest/tests/policy_CookiesBlockedForUrls/'
      'control.notset_allow')


def main(argv):
  if len(argv) < 1:
    print 'git_bisect.py index'
    sys.exit(1)

  utils.AssertCWD(utils.CHROME_DIR)
  CreateBranch(int(argv[1]))
  RunTest()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
