#!/usr/bin/python

import argparse
import sys

import utils


def Script(opts):
  pass


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Script')
  return utils.ParseArgs(parser, argv)


def main(argv):
  opts = ParseArgs(argv)
  Script(opts)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
