#!/usr/bin/python

import argparse
import sys

import git_lib
import utils


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Checkout a release branch')
  parser.add_argument('--branch', help='branch to check out')
  parser.add_argument('--force', action='store_true', default=False,
                      help='delete existing branch')
  return parser.parse_known_args(argv[1:])


def main(argv):
  utils.AssertCWD(utils.CHROME_DIR)
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)
  git_lib.CheckoutRelease(opts.branch, opts.force)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
