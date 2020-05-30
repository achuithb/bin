#!/usr/bin/python

import argparse
import sys

import utils


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Script')
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
