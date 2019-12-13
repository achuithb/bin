#!/usr/bin/python

import os, sys, subprocess

import utils

#TODO: Use argparse for these.
DEFAULT_DEPTH = 7
CACHE_DEPTH = 4
MIN_SIZE = 10  # Skip anything less than 10G.

CHROOT_CACHE = os.path.join(utils.CROS_DIR, 'chroot/var/cache')
CHROOT = os.path.join(utils.CROS_DIR, 'chroot.img')


def InGig(size):
  return size/(1024 * 1024)


def PrintUsageForDir(ary):
  print '%s: %dG' % (ary[1], InGig(ary[0]))
  sys.stdout.flush()


def DiskUsage(d):
  ary = utils.RunCmd(['sudo', 'du', '-s', d], silent=True).rstrip().split()
  ary[0] = int(ary[0])
  #print ary
  return ary  # (numblocks, name)


def PrintUsageForChroot():
  row = DiskUsage(CHROOT)
  row[1] = os.path.relpath(row[1], utils.HOME_DIR)
  PrintUsageForDir(row)


def PrintTotalUsage(cols, depth):
  for row in sorted(cols, reverse=True, key=lambda a: a[0]):
    if InGig(row[0]) < MIN_SIZE:
      break;
    PrintUsageForDir(row)
    if row[1] == 'code/cros':
      PrintUsageForChroot()
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


def DF():
  res = utils.RunCmd('df -h', silent=True).rstrip().split('\n')
  k = res[0].split()
  for r in res:
    v = r.split()
    # print v
    if v[0] == 'objfsd':
      print('%s=%s, %s=%s, %s=%s, %s=%s' % (
          k[1], v[1], k[2], v[2], k[3], v[3], k[4], v[4]))


def DefaultDirs():
  DF()
  DefaultDir(utils.CODE_DIR, DEFAULT_DEPTH)
  print '\n%s' % os.path.relpath(CHROOT_CACHE, utils.HOME_DIR)
  DefaultDir(CHROOT_CACHE, CACHE_DEPTH)


def main(argv):
  dirs = argv[1:]
  if dirs:
    UsageForDirs(dirs, DEFAULT_DEPTH)
  else:
    DefaultDirs()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
