#!/usr/bin/python

import os
import re
import subprocess

def AbsPath(path=''):
  return os.path.realpath(os.path.join(os.environ['HOME'], path))

HOME_DIR = AbsPath()
CODE_DIR = AbsPath('code')
BIN_DIR = AbsPath('code/bin')
CROS_DIR = AbsPath('code/cros')
CHROME_DIR = AbsPath('code/chrome/src')
CATAPULT_DIR = AbsPath('code/catapult')
ANDROID_DIR = AbsPath('code/android')

dry_run = False

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN = range(7)

def ColorPrint(color, text):
  color = '\033[1;%dm' % (30 + color)
  reset = '\033[0m'
  print(color + text + reset)


def RunCmd(args, call=False, silent=False, dryrun=None):
  if dryrun is None:
    global dry_run
    dryrun = dry_run

  if isinstance(args, str):
    args = args.split()
  if not isinstance(args, list):
    raise Exception('RunCmd: malformed cmd %r' % args)

  if not silent:
    ColorPrint(CYAN, 'RunCmd: %s' % (' ').join(args))
  if dryrun:
    return 0
  if call:
    ret = subprocess.call(args)
  else:
    ret = subprocess.check_output(args)
    if not silent:
      print(ret)
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

def IsAndroid(root=False):
  return _IsPlatform(ANDROID_DIR, root)


def AssertCWD(paths):
  if isinstance(paths, str):
    paths = [paths]
  if not isinstance(paths, list):
    raise Exception('%s should be an array of paths' % paths)

  for path in paths:
    path = os.path.realpath(path)
    if os.path.commonprefix([path, os.getcwd()]) == path:
      return
  msg = 'Not at expected path(s): %r' % [
      os.path.basename(path) for path in paths
  ]
  ColorPrint(RED, msg)
  raise Exception(msg)


def _PrintMatch(m):
  print(m.string.rstrip())


def SearchFile(filename, search_exp=r'.*', Process=_PrintMatch):
  with open(filename, 'r') as f:
    for line in f:
      m = re.search(search_exp, line)
      if m:
        Process(m)


def ParseArgs(parser, argv, raise_on_rem=True):
  parser.add_argument('--dry-run', action='store_true', default=False,
                      help='Dry run')
  opts, rem = parser.parse_known_args(argv[1:])

  if rem and raise_on_rem:
    raise Exception('Unknown args: %s' % rem)
  if opts.dry_run:
    global dry_run
    dry_run = True

  if raise_on_rem:
    return opts
  else:
    return opts, rem


#TODO: Move somewhere else.
def GclientSync():
  if IsChrome():
    RunCmd('gclient sync -D -j16', call=True)
