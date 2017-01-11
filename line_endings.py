#!/usr/bin/python

import sys

with open(sys.argv[1]) as f:
  count = 0
  for line in f:
    count += 1
    if line.find('\\r\\n'):
      print '%d:%s' % (count, line)

