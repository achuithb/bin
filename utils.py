#!/usr/bin/python

import os
import subprocess

def AbsPath(path):
  return os.path.realpath(os.path.join(os.environ['HOME'], path))

CROS_DIR = AbsPath('code/cros')
CHROME_DIR = AbsPath('code/chrome/src')
CATAPULT_DIR = AbsPath('code/catapult')

dry_run = False

def RunCmd(args, call=False, silent=False):
  if isinstance(args, str):
    args = args.split()
  if not isinstance(args, list):
    raise Exception('RunCmd: malformed cmd %r' % args)

  if not silent:
    print 'RunCmd: %s' % (' ').join(args)
  if dry_run:
    return 0
  if call:
    ret = subprocess.call(args)
  else:
    ret = subprocess.check_output(args)
    if not silent:
      print ret
  return ret


def IsCrOS():
  return os.getcwd().startswith(utils.CROS_DIR)


def AssertCWD(paths):
  if isinstance(paths, str):
    paths = [paths]
  if not isinstance(paths, list):
    raise Exception('%s should be an array of paths' % paths)

  for path in paths:
    path = os.path.realpath(path)
    if os.path.commonprefix([path, os.getcwd()]) == path:
      return
  raise Exception('Not at expected path(s) %r' % paths)

