#!/usr/bin/python

import sys

import cros_utils
import utils


def main(argv):
  utils.AssertCWD(utils.CROS_DIR)
  cros_utils.CheckoutMaster()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
