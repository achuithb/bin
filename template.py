#!/usr/bin/python

import argparse
import sys

import utils


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Script')
  parser.add_argument('--dry-run', action='store_true', default=False,
                      help='dry run')
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
