#!/usr/bin/python

import os, sys

import utils


CLEAN_DIRS = [
    os.path.join(utils.CROS_DIR, w) for w in [
        'chromite',
        'src/platform/dev',
    ]
]


def main(argv):
  for d in CLEAN_DIRS:
    utils.RunCmd(['pyclean', d])


if __name__ == '__main__':
  sys.exit(main(sys.argv))
