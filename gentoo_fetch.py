#!/usr/bin/python

import os
import sys

import utils

EBUILD = 'blas-reference-20070226-r4.ebuild'
PACKAGE = 'sci-libs/blas-reference'
PATCHES = [
  'blas-reference-20070226-autotool.patch',
  'blas-reference-20070226-pkg-config.patch',
  'eselect.blas.reference',
  'eselect.blas.reference-r1',
]
GIT_ID = '4739b0a41d6e1a1e827f8df9384ee2d4d4ab5466'
HTTP_PATH = 'https://gitweb.gentoo.org/repo/gentoo.git/plain/%s/%s?id=%s'
DEFAULT_FILES = ['Manifest', 'metadata.xml']

def main(argv):
  files = DEFAULT_FILES + [EBUILD]
  for patch in PATCHES:
    files += ['files/%s' % patch]
  if len(PATCHES):
    os.mkdir('files')
  for filename in files:
    http_path = HTTP_PATH % (PACKAGE, filename, GIT_ID)
    with open(filename, 'w') as fd:
      fd.write(utils.RunCmd('curl %s' % http_path))

if __name__ == '__main__':
  sys.exit(main(sys.argv))
