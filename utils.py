#!/usr/bin/python

import os
import subprocess

def AbsPath(path):
  return os.path.realpath(os.path.join(os.environ['HOME'], path))

CROS_DIR = AbsPath('code/cros')
CHROME_DIR = AbsPath('code/chrome/src')
CATAPULT_DIR = AbsPath('code/catapult')

dry_run = False

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def ColorPrint(color, text):
  color = '\033[1;%dm' % (30 + color)
  reset = '\033[0m'
  print(color + text + reset)


def RunCmd(args, call=False, silent=False, dry_run=dry_run):
  if isinstance(args, str):
    args = args.split()
  if not isinstance(args, list):
    raise Exception('RunCmd: malformed cmd %r' % args)

  if not silent:
    ColorPrint(CYAN, 'RunCmd: %s' % (' ').join(args))
  if dry_run:
    return 0
  if call:
    ret = subprocess.call(args)
  else:
    ret = subprocess.check_output(args)
    if not silent:
      print ret
  return ret


def _IsPlatform(root_path, root):
  cwd = os.getcwd()
  return cwd == root_path if root else cwd.startswith(root_path)

def IsCrOS(root=False):
  return _IsPlatform(CROS_DIR, root)

def IsChrome(root=False):
  return _IsPlatform(CHROME_DIR, root)

def IsCatapult(root=False):
  return _IsPlatform(CATPULT_DIR, root)


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


def GclientSync():
  if IsChrome():
    RunCmd('gclient sync -D -j16', call=True)


def RepoRebase(dirs):
  if not dirs and IsCrOS(root=True):
    ColorPrint(RED, 'Must specify directories to rebase.')
    sys.exit(1)

  import git_lib

  if not dirs:
    dirs = ['.']
  cwd = os.getcwd()
  for d in dirs:
    ColorPrint(BLUE, 'Rebasing %s' % d)
    os.chdir(d)
    git_lib.GitRebaseAll()
    git_lib.GitCheckoutMaster()
    os.chdir(cwd)
