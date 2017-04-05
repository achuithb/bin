#!/usr/bin/python

import os, sys, subprocess


def CheckOutput(args):
  return subprocess.check_output(args.split(' '))


def PrintUsage(ary):
  print "".join(word.ljust(20) for word in reversed(ary))


def DiskUsage(d):
  return CheckOutput('sudo du -hs %s' % d).rstrip().split()


def SortFunc(a):
  val = a[0]
  m = val[-1]
  n = val[0:len(val)-1]
  n = float(n) if n else 0  # Handle empty string.
  if m == 'K': n *= 1024
  if m == 'M': n *= 1024 * 1024
  if m == 'G': n *= 1024 * 1024 * 1024
  return n

def PrintTotalUsage(cols):
  for row in sorted(cols, reverse=True, key=SortFunc):
    if row[0].find('G') == -1:
      break;  # Skip anything less than a gig.
    PrintUsage(row)


def TotalUsage(dirs):
  cols = []
  for d in dirs:
    # Skip non-directories.
    if os.path.isdir(d):
      cols.append(DiskUsage(d))
  return cols


def main(argv):
  cols = TotalUsage(argv[1:])
  PrintTotalUsage(cols)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
