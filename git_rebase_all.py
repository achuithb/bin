#!/usr/bin/python

import sys

import git_lib

def main(argv):
  git_lib.GitRebaseAll()

if __name__ == '__main__':
  sys.exit(main(sys.argv))

