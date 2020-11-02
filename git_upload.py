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


def main(argv):
  utils.AssertCWD([utils.CROS_DIR, utils.CHROME_DIR, utils.CATAPULT_DIR])
  Upload(argv[1:])


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Upload a CL')
  parser.add_argument('--no-verify', dest='verify', action='store_false',
                      default=True, help='disable verification')
  parser.add_argument('--no-upstream', dest='upstream', action='store_false',
                      default=True, help="don't change upstream branch")
  parser.add_argument('--dry-run', action='store_true', default=False,
                      help='Dry run')
  return parser.parse_known_args(argv[1:])


def main(argv):
  utils.AssertCWD([utils.CROS_DIR, utils.CHROME_DIR, utils.CATAPULT_DIR])
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)
  if opts.dry_run:
    utils.dry_run = True

  Upload(opts.verify, opts.upstream)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
