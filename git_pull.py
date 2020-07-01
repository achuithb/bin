#!/usr/bin/python

import argparse
import os
import sys

import chromite_setup
import cros_utils
import cros_paths
import git_lib
import utils


def CheckoutMaster():
  if utils.IsCrOS():
    cros_utils.CheckoutCrosMaster()
  else:
    if utils.IsChrome():
      os.chdir(chromite_setup.CHROME_DIR)
      if not git_lib.DetachedHead():
        raise Exception('chromite branch active.')
      os.chdir(utils.CHROME_DIR)
    git_lib.GitCheckoutMaster()


def Pull():
  if utils.IsCrOS():
    utils.RunCmd('repo sync', call=True)
  else:
    git_lib.GitPull()


def Sync():
  utils.GclientSync()


def Rebase():
  if utils.IsCrOS():
    cros_utils.RepoRebase()
  else:
    git_lib.GitRebaseAll()


def Finish():
  if utils.IsCrOS():
    os.chdir(cros_paths.SCRIPTS_DIR)
    git_lib.GitCheckout(cros_utils.SCRIPTS_BASH_COMPLETION)
    os.chdir(utils.CROS_DIR)


def All():
  CheckoutMaster()
  Pull()
  Sync()
  Rebase()
  Finish()


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Script')
  parser.add_argument('--checkout-master', action='store_true', default=False)
  parser.add_argument('--pull', action='store_true', default=False)
  parser.add_argument('--sync', action='store_true', default=False)
  parser.add_argument('--rebase', action='store_true', default=False)
  parser.add_argument('--finish', action='store_true', default=False)
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

  if opts.checkout_master:
    CheckoutMaster()
  if opts.pull:
    Pull()
  if opts.sync:
    Sync()
  if opts.rebase:
    Rebase()
  if opts.finish:
    Finish()
  if len(argv) == 1:
    All()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
