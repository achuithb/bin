#!/usr/bin/python

import subprocess

dry_run = False

def RunCmd(args, call=False):
  if isinstance(args, str):
    args = args.split()
  if not isinstance(args, list):
    raise Exception('RunCmd: malformed cmd %r' % args)

  print 'RunCmd: %s' % (' ').join(args)
  if dry_run:
    return 0
  if call:
    ret = subprocess.call(args)
  else:
    ret = subprocess.check_output(args)
    print ret
  return ret

