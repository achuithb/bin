#!/usr/bin/python

import argparse
import sys

import utils


total = 0
def Process(m):
  c = m.group(1)
  # print(m.string)
  global total
  total += int(c)


def Run(filename):
  utils.SearchFile(filename, search_exp=r'\((\d+)\)', Process=Process)
  global total
  print(total)


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Parse Kernel log file')
  parser.add_argument('--file')
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

  if not opts.file:
    raise Exception('Must specify file.')

  Run(opts.file)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
