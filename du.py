#!/usr/bin/python

import argparse
import subprocess
import sys
import os

import utils


CHROOT_CACHE = os.path.join(utils.CROS_DIR, 'chroot/var/cache')
CHROOT_IMG = os.path.join(utils.CROS_DIR, 'chroot.img')


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
  row = DiskUsage(CHROOT_IMG)
  row[1] = os.path.relpath(row[1], utils.HOME_DIR)
  PrintUsageForDir(row)


def PrintTotalUsage(cols, depth, min_size):
  for row in sorted(cols, reverse=True, key=lambda a: a[0]):
    if InGig(row[0]) < min_size:
      break;
    PrintUsageForDir(row)
    if row[1] == 'code/cros':
      PrintUsageForChroot()
    Recurse(row[1], depth, min_size)


def Recurse(root, depth, min_size):
  if not depth:
    return
  dirs = os.listdir(root)
  for i in range(len(dirs)):
    dirs[i] = os.path.join(root, dirs[i])
  #print dirs
  UsageForDirs(dirs, depth-1, min_size)


def UsageForDirs(dirs, depth, min_size):
  cols = []
  for d in dirs:
    # Skip non-directories.
    if os.path.isdir(d):
      cols.append(DiskUsage(d))
  PrintTotalUsage(cols, depth, min_size)


def DF():
  res = utils.RunCmd('df -h', silent=True).rstrip().split('\n')
  k = res[0].split()
  for r in res:
    v = r.split()
    # print v
    if v[0] == 'objfsd':
      print('%s=%s, %s=%s, %s=%s, %s=%s' % (
          k[1], v[1], k[2], v[2], k[3], v[3], k[4], v[4]))


def DefaultDir(path, depth, min_size):
  os.chdir(os.path.dirname(path))
  UsageForDirs([os.path.basename(path)], depth, min_size)


def DefaultDirs(cache_depth, min_size):
  DF()
  DefaultDir(utils.CODE_DIR, cache_depth, min_size)
  if os.path.exists(CHROOT_CACHE):
    print '\n%s' % os.path.relpath(CHROOT_CACHE, utils.HOME_DIR)
    DefaultDir(CHROOT_CACHE, cache_depth, min_size)
  DefaultDir(os.path.join(utils.HOME_DIR, 'Downloads'), cache_depth, min_size)


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Disk usage')
  parser.add_argument('--depth', type=int, default=7, help='default depth')
  parser.add_argument('--cache-depth', type=int, default=4, help='cache depth')
  parser.add_argument('--size', type=int, default=10, help='size cutoff in GB')
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)

  if rem:
    UsageForDirs(rem, opts.depth, opts.size)
  else:
    DefaultDirs(opts.cache_depth, opts.size)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
