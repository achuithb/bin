#!/usr/bin/python

import sys

import cros_utils
import utils


def main(argv):
  utils.AssertCWD(utils.CROS_DIR)
  dirs = argv[1:] if len(argv) else None
  cros_utils.CheckoutMaster(dirs)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
