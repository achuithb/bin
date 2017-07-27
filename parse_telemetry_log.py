#!/usr/bin/python

import os, re, sys


def Parse(filename):
  with open(filename) as f:
    count = 0
    for line in f:
      match = re.compile('(\S+) failed unexpectedly').search(line)
      if match:
        print match.group(1)
        count += 1
    print '%d failures' % count


def Usage(argv):
  print 'Usage: %s [file]' % argv[0].split('/')[-1]
  sys.exit(1)

def main(argv):
  if len(argv) != 2 or not os.path.isfile(argv[1]):
    Usage(argv)
  Parse(argv[1])

if __name__ == '__main__':
  sys.exit(main(sys.argv))
