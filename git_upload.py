#!/usr/bin/python

import sys

import git_lib
import utils

def RepoUpload(args):
  cmd = 'repo upload . --cbr '
  cmd += '--verify' if presubmit else '--no-verify'
  utils.RunCmd(cmd, call=True)


def Upload(args):
  presubmit = True
  if args:
    if args[0] == '--no-presubmit':
      presubmit = False
    else:
      print 'Did you mean --no-presubmit?'
      sys.exit(1)

  if utils.IsCrOS():
    RepoUpload(presubmit)
  else:
    git_lib.GitSetUpstream('origin/master')
    git_lib.GitUpload(presubmit)
    git_lib.GitSetUpstream('master')


def main(argv):
  utils.AssertCWD([utils.CROS_DIR, utils.CHROME_DIR, utils.CATAPULT_DIR])
  Upload(argv[1:])


if __name__ == '__main__':
  sys.exit(main(sys.argv))
