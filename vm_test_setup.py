#!/usr/bin/python

import os
import subprocess
import sys

# Run this script from ~/code/chrome/src/third_party/chromite/
# on master branch.

BASE_DIR = '/usr/local/google/home/achuith/code/'
CROS_DIR = os.path.join(BASE_DIR, 'cros/chromite')
CHROME_DIR = os.path.join(BASE_DIR, 'chrome/src/third_party/chromite')
FILES = [
    'scripts/cros_run_vm_test.py',
    'scripts/cros_vm.py',
]

def DetachedHead():
  return subprocess.check_output(
    ['git', 'status', '-sb']).rstrip() == '## HEAD (no branch)'


def GitBranch():
  return subprocess.check_output(
    ['git', 'symbolic-ref', '--short', 'HEAD']).rstrip()


def CreateGitBranch(new_branch):
  subprocess.call(['git', 'checkout', '-b', new_branch])


def GitAddFile(filename):
  subprocess.call(['git', 'add', filename])


def GitCommit():
  subprocess.call(['git', 'commit', '-a', '-m', 'vm_test debugging'])


def RemoveFile(filename):
  try:
    os.unlink(filename)
  except OSError:
    pass


def CreateLink(filename):
  print filename
  source = os.path.join(CROS_DIR, filename)
  link = os.path.join(CHROME_DIR, filename)
  RemoveFile(link)
  os.symlink(source, link)
  GitAddFile(link)


def main(argv):
  if os.path.commonprefix([CHROME_DIR, os.getcwd()]) != CHROME_DIR:
    raise Exception('Not at %s' % CHROME_DIR)
  if not DetachedHead():
    raise Exception('Not in detached head state.')

  CreateGitBranch('master')
  CreateGitBranch('vm_test')
  for filename in FILES:
    CreateLink(filename)
  GitCommit()


if __name__ == '__main__':
  sys.exit(main(sys.argv))

