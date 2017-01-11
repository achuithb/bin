#!/usr/bin/python

import sys, subprocess


def CheckOutput(args):
  return subprocess.check_output(args.split(' '))


def PrintUsage(ary):
  print "".join(word.ljust(20) for word in reversed(ary))


def DiskUsage(d):
  return CheckOutput('sudo du -hs %s' % d).rstrip().split()


def PrintTotalUsage(cols):
  def SortFunc(a):
    val = a[0]
    m = val[-1]
    n = float(val[0:len(val)-1])
    if m == 'K': n *= 1024
    if m == 'M': n *= 1024 * 1024
    if m == 'G': n *= 1024 * 1024 * 1024
    return n
  for row in sorted(cols, reverse=True, key=SortFunc):
    PrintUsage(row)


def TotalUsage(dirs):
  cols = []
  for d in dirs:
    cols.append(DiskUsage(d))
  return cols


def main(argv):
  cols = TotalUsage(argv[1:])
  PrintTotalUsage(cols)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
