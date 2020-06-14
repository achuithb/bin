#!/usr/bin/python

import sys

import git_lib
import utils

def RepoUpload(verify):
  cmd = 'repo upload . --cbr '
  cmd += '--verify' if verify else '--no-verify'
  utils.RunCmd(cmd, call=True)


def Upload(args):
  verify = True
  if args:
    if args[0] == '--no-verify':
      verify = False
    else:
      print 'Did you mean --no-verify?'
      sys.exit(1)

  if utils.IsCrOS():
    RepoUpload(verify)
  else:
    git_lib.GitSetUpstream(git_lib.ORIGIN_MASTER)
    git_lib.GitUpload(verify)
    git_lib.GitSetUpstream(git_lib.MASTER)


def main(argv):
  utils.AssertCWD([utils.CROS_DIR, utils.CHROME_DIR, utils.CATAPULT_DIR])
  Upload(argv[1:])


if __name__ == '__main__':
  sys.exit(main(sys.argv))
