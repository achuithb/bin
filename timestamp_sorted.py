#!/usr/bin/python

import re
import decimal

def duration(line):
  d = re.compile('passed ([^s]+)s').search(line).group(1)
  return int(decimal.Decimal(d) * 10000)

def compare(x,y):
  return duration(x) < duration(y)

def main():
  with open('passed.log') as f:
    lines = f.readlines()
  lines = [l.rstrip() for l in lines]
  lines = sorted(lines, key=duration)
  for line in lines:
    print line


if __name__ == '__main__':
  main()
