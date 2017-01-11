#!/usr/bin/python
import sys
import subprocess

def main(argv):
  f = open('histograms.xml')
  n = ''
  for l in f.readlines():
    if l.startswith('<histogram name='):
      n = l
    if l.startswith("  <owner>Please list the metric's owners. Add more owner tags as needed.</owner>"):
      print n.strip()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
