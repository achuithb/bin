#!/usr/bin/python

import sys

import utils


def Usage(argv):
  print 'Usage: %s' % argv[0].split('/')[-1]
  sys.exit(1)


def main(argv):
  if len(argv) < 1:
    Usage(argv)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
