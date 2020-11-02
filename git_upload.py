#!/usr/bin/python

import argparse
import sys

import git_lib
import utils

def RepoUpload(verify):
  cmd = 'repo upload . --cbr '
  cmd += '--verify' if verify else '--no-verify'
  utils.RunCmd(cmd, call=True)


def Upload(verify, upstream):
  if utils.IsCrOS():
    RepoUpload(verify)
  else:
    if upstream:
      git_lib.GitSetUpstream(git_lib.ORIGIN_MASTER)
    git_lib.GitUpload(verify)
    if upstream:
      git_lib.GitSetUpstream(git_lib.MASTER)


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Upload a CL')
  parser.add_argument('--no-verify', dest='verify', action='store_false',
                      default=True, help='disable verification')
  parser.add_argument('--no-upstream', dest='upstream', action='store_false',
                      default=True, help="don't change upstream branch")
  return utils.ParseArgs(parser, argv)


def main(argv):
  utils.AssertCWD([utils.CROS_DIR, utils.CHROME_DIR, utils.CATAPULT_DIR])
  opts = ParseArgs(argv)
  Upload(opts.verify, opts.upstream)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
