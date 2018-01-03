#!/usr/bin/python

import os, sys, subprocess

import utils

#TODO: Use argparse for these.
DEFAULT_DEPTH = 7
CACHE_DEPTH = 4
MIN_SIZE = 10  # Skip anything less than 10G.

HOME = '/usr/local/google/home/achuith'
CODE = os.path.join(HOME, 'code')
CACHE = os.path.join(HOME, 'code/cros/chroot/var/cache')


def PrintUsageForDir(ary):
  print '%s: %dG' % (ary[1], ary[0])


def DiskUsage(d):
  ary = utils.RunCmd(['sudo', 'du', '-s', d], silent=True).rstrip().split()
  ary[0] = int(ary[0])
  #print ary
  return ary  # (numblocks, name)


def PrintTotalUsage(cols, depth):
  for row in sorted(cols, reverse=True, key=lambda a: a[0]):
    row[0] = row[0]/(1024 * 1024)
    if row[0] < MIN_SIZE:
      break;
    PrintUsageForDir(row)
    Recurse(row[1], depth)


def Recurse(root, depth):
  if not depth:
    return
  dirs = os.listdir(root)
  for i in range(len(dirs)):
    dirs[i] = os.path.join(root, dirs[i])
  #print dirs
  UsageForDirs(dirs, depth-1)


def UsageForDirs(dirs, depth):
  cols = []
  for d in dirs:
    # Skip non-directories.
    if os.path.isdir(d):
      cols.append(DiskUsage(d))
  PrintTotalUsage(cols, depth)


def DefaultDir(path, depth):
  os.chdir(os.path.dirname(path))
  UsageForDirs([os.path.basename(path)], depth)


def DefaultDirs():
  DefaultDir(CODE, DEFAULT_DEPTH)
  print '\n%s' % CACHE
  DefaultDir(CACHE, CACHE_DEPTH)


def main(argv):
  dirs = argv[1:]
  if dirs:
    UsageForDirs(dirs, DEFAULT_DEPTH)
  else:
    DefaultDirs()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
