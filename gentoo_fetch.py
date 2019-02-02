#!/usr/bin/python

import argparse
import os
import sys

import utils

PATCHES = [
]
HTTP_PATH = ('https://gitweb.gentoo.org/repo/gentoo.git/plain/%s/%s?id='
             '4739b0a41d6e1a1e827f8df9384ee2d4d4ab5466')

DEFAULT_FILES = ['Manifest', 'metadata.xml']

def ParseArgs(argv):
  parser = argparse.ArgumentParser('Script to fetch Gentoo Package files')
  parser.add_argument('--ebuild', help='Name of ebuild')
  parser.add_argument('--patches', nargs='*', help='Patch files.')
  return parser.parse_args(argv[1:])


def MkDir(patches):
  if patches:
    try:
      os.mkdir('files')
    except OSError:
      pass


def CreateFileList(ebuild, patches):
  files = DEFAULT_FILES + [ebuild]
  for patch in patches:
    files += ['files/%s' % patch]
  return files


def FetchFiles(files):
  cwd = os.getcwd()
  root = os.path.dirname(os.path.dirname(cwd))
  package = os.path.relpath(cwd, root)
  for filename in files:
    http_path = HTTP_PATH % (package, filename)
    with open(filename, 'w') as fd:
      fd.write(utils.RunCmd('curl %s' % http_path))


def main(argv):
  opts = ParseArgs(argv)
  MkDir(opts.patches)
  FetchFiles(CreateFileList(opts.ebuild, opts.patches))


if __name__ == '__main__':
  sys.exit(main(sys.argv))
