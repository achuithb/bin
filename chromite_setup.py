#!/usr/bin/python

import os
import subprocess
import sys

# Run this script from ~/code/chrome/src/third_party/chromite/
# on master branch.

BASE_DIR = '/usr/local/google/home/achuith/code/'
CROS_DIR = os.path.join(BASE_DIR, 'cros/chromite')
CHROME_DIR = os.path.join(BASE_DIR, 'chrome/src/third_party/chromite')
MASTER_BRANCH = 'master'
VM_TEST_BRANCH = 'chromite'
FILES = [
    'scripts/cros_run_vm_test.py',
    'scripts/cros_vm.py',
    'cli/cros/cros_chrome_sdk.py',
]

def DetachedHead():
  return subprocess.check_output(
    ['git', 'status', '-sb']).rstrip() == '## HEAD (no branch)'


def GitBranch():
  return subprocess.check_output(
    ['git', 'symbolic-ref', '--short', 'HEAD']).rstrip()


def GitCreateBranch(new_branch):
  subprocess.call(['git', 'checkout', '-b', new_branch])


def GitDeleteBranch(branch):
  subprocess.call(['git', 'branch', '-D', branch])


def GitCheckoutHEAD():
  subprocess.call(['git', 'checkout', 'HEAD~'])


def GitAddFile(filename):
  subprocess.call(['git', 'add', filename])


def GitCommit():
  subprocess.call(['git', 'commit', '-a', '-m', 'chromite debugging'])


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

def Create():
  if not DetachedHead():
    raise Exception('Not in detached head state.')

  GitCreateBranch(MASTER_BRANCH)
  GitCreateBranch(VM_TEST_BRANCH)
  for filename in FILES:
    CreateLink(filename)
  GitCommit()

def Delete():
  if GitBranch() != VM_TEST_BRANCH:
    raise Exception('Not in expected branch %s.' % VM_TEST_BRANCH)

  GitCheckoutHEAD()
  GitDeleteBranch(MASTER_BRANCH)
  GitDeleteBranch(VM_TEST_BRANCH)


def Usage(argv):
  print 'Usage: %s [create|delete]' % argv[0].split('/')[-1]
  sys.exit(1)


def main(argv):
  if os.path.commonprefix([CHROME_DIR, os.getcwd()]) != CHROME_DIR:
    raise Exception('Not at %s' % CHROME_DIR)

  func_map = { 'create': Create, 'delete': Delete }
  if len(argv) != 2 or argv[1] not in func_map.keys():
    Usage(argv)
  func_map[argv[1]]()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
