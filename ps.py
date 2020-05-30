#!/usr/bin/python

import argparse
import sys

import utils


def PS(mem, num):
  sort = '--sort=-%' + ('mem' if mem else 'cpu')
  ary = utils.RunCmd([
      'ps', '-eo', 'pid,ppid,%cpu,%mem,cmd', sort],
                     silent=True).split('\n')
  for i in range(num):
    print(ary[i])


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Top processes by cpu/mem')
  parser.add_argument('--mem', action='store_true', default=False,
                      help='sort by memory instead of cpu')
  parser.add_argument('--num', default=7, help='number of processes')
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, _ = ParseArgs(argv)
  PS(opts.mem, opts.num)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
