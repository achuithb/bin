#!/usr/bin/python

import os, sys

import git_lib
import utils

def Usage():
  print 'git_bisect.py index'
  sys.exit(1)

def CreateBranch(index):
  # open commit file
  with open('commit.txt') as f:
    lines = f.read().splitlines()
  # commit <hash>
  _, commit = lines[index].split()
  git_lib.GitCreateBranch('bisect_%d' % index, commit)
  utils.GclientSync()

def Gen():
  # This doesn't work.
  utils.RunCmd(['gn', 'gen', 'out_amd64-generic/Release', "--args='%s'" %
                os.environ['GN_ARGS'].replace('\n', ', ')])

def RunTest():
  utils.RunCmd(
      'cros_run_vm_test --build --deploy --build-dir=out_amd64-generic/Release '
      '--cmd -- /usr/local/autotest/bin/autotest '
      '/usr/local/autotest/tests/policy_CookiesBlockedForUrls/'
      'control.notset_allow')


def main(argv):
  if len(argv) < 1:
    Usage()

  index = int(argv[1])
  utils.AssertCWD(utils.CHROME_DIR)
  CreateBranch(index)
  # Gen()
  RunTest()


if __name__ == '__main__':
  sys.exit(main(sys.argv))