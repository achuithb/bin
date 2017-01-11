#!/usr/bin/python
import sys
import subprocess

def main(argv):
  f = open('pyauto_api.txt')
  comment = False
  for l in f.readlines():
    if comment:
      comment = False
      print l
    if l.startswith('  def '):
      print l.rstrip()
      comment = True

if __name__ == '__main__':
  sys.exit(main(sys.argv))
