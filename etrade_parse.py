#!/usr/bin/python

import argparse
import os
import sys

import utils


DEFAULT_DIR=os.path.join(utils.HOME_DIR, 'Documents', 'etrade')
FILENAME = 'etrade_{year}.txt'

total = 0
def Process(m):
  c = m.group(1)
  # print(m.string)
  global total
  total += int(c)


def Run(filename):
  # utils.SearchFile(filename, r'\((\d+)\)', Process)
  pass


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Parse Etrade bank statements')
  parser.add_argument('--year')
  parser.add_argument('--dir', help='directory with bank statements '
                      ' in format %s' % FILENAME, default=DEFAULT_DIR)
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

  if not opts.year:
    raise Exception('Must specify year.')

  filename = os.path.join(opts.dir, FILENAME.format(year=opts.year))
  print filename
  # Run(filename)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
