#!/usr/bin/python

import argparse
import sys

import utils

SEARCH_TERM = r'0\t0'

def ParseArgs(argv):
  parser = argparse.ArgumentParser('Search Script')
  parser.add_argument('--file', help='File to search')
  parser.add_argument('--term', default=SEARCH_TERM,
                      help='Term to search')
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

  if not opts.file:
    raise Exception('Must specify --file.')

  utils.SearchFile(opts.file, opts.term)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
