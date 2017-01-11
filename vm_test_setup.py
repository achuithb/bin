#!/usr/bin/python

import os
import subprocess
import sys

# Run this script from ~/code/chrome/src/third_party/chromite/
# on master branch.

VM_BRANCH = 'vm_test'
BASE_DIR = '/usr/local/google/home/achuith/code/'
CROS_DIR = os.path.join(BASE_DIR, 'cros/chromite')
CHROME_DIR = os.path.join(BASE_DIR, 'chrome/src/third_party/chromite')
FILES = [
    'bin/cros_run_vm_test',
    'bin/cros_vm',
    'scripts/cros_run_vm_test.py',
    'scripts/cros_vm.py',
    'cbuildbot/constants.py',
    'cli/cros/cros_chrome_sdk.py',
]


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
  if os.getcwd() != CHROME_DIR:
    raise Exception('not at %s' % CHROME_DIR)
  if GitBranch() != 'master':
    raise Exception('not on master')

  CreateGitBranch(VM_BRANCH)
  for filename in FILES:
    CreateLink(filename)
  GitCommit()


if __name__ == '__main__':
  sys.exit(main(sys.argv))

