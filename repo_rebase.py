#!/usr/bin/python

import sys

import utils


def main(argv):
  dirs = argv[1:] if len(argv) else None
  utils.RepoRebase(dirs)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
