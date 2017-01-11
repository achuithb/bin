#!/usr/bin/python

import sys
import subprocess

def remove_whitespace(filename):
  print 'Removing whitespace from ' + filename
  subprocess.call(['wc', '-c', filename])
  with open(filename, 'r') as f:
    unstripped = f.readlines()
  with open(filename, 'w') as f:
    for line in unstripped:
      f.write(line.rstrip() + '\n')
  subprocess.call(['wc', '-c', filename])

def main(argv):
  for filename in argv[1:]:
    remove_whitespace(filename)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
