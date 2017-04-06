#!/usr/bin/python

import os, sys, subprocess

#TODO(achuith): Use argparse for these.
MIN_SIZE = 10  # Skip anything less than 10G.
MAX_DEPTH = 7
HOME = '/usr/local/google/home/achuith'

def CheckOutput(args):
  #print args
  return subprocess.check_output(args).rstrip()

def PrintUsageForDir(ary):
  print '%s: %dG' % (ary[1], ary[0])

def DiskUsage(d):
  ary = subprocess.check_output(['sudo', 'du', '-s', d]).rstrip().split()
  ary[0] = int(ary[0])
  #print ary
  return ary  # (numblocks, name)

def PrintTotalUsage(cols):
  for row in sorted(cols, reverse=True, key=lambda a: a[0]):
    row[0] = row[0]/(1024 * 1024)
    if row[0] < MIN_SIZE:
      break;
    PrintUsageForDir(row)
    Recurse(row[1])

def Recurse(root):
  if root.count('/') >= MAX_DEPTH:
    return
  dirs = os.listdir(root)
  for i in range(len(dirs)):
    dirs[i] = os.path.join(root, dirs[i])
  #print dirs
  UsageForDirs(dirs)

def UsageForDirs(dirs):
  cols = []
  for d in dirs:
    # Skip non-directories.
    if os.path.isdir(d):
      cols.append(DiskUsage(d))
  PrintTotalUsage(cols)


def main(argv):
  dirs = argv[1:]
  if not dirs:
    os.chdir(HOME)
    dirs = ['code']
  UsageForDirs(dirs)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
