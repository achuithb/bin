#!/usr/bin/python

import sys

import git_lib
import utils

def RepoUpload(args):
  cmd = 'repo upload . --cbr '
  cmd += args[0] if args and args[0] == '--no-verify' else '--verify'
  utils.RunCmd(cmd, call=True)


def Upload(args):
  if utils.IsCrOS():
    RepoUpload(args)
  else:
    git_lib.GitSetUpstream('origin/master')
    git_lib.GitUpload()
    git_lib.GitSetUpstream('master')


def main(argv):
  utils.AssertCWD([utils.CROS_DIR, utils.CHROME_DIR, utils.CATAPULT_DIR])
  Upload(argv[1:])


if __name__ == '__main__':
  sys.exit(main(sys.argv))
