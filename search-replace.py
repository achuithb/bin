#!/usr/bin/python

import sys

search = 'NetworkPortalDetector::Get'
replace = 'network_portal_detector::GetInstance'

def search_replace(filename):
  print 'Replacing in ' + filename
  with open(filename, 'r') as f:
    filetext = f.readlines()
  with open(filename, 'w') as f:
    for line in filetext:
      f.write(line.replace(search, replace))

def main(argv):
  filelist = argv[1]
  with open(filelist, 'r') as fl:
    for f in fl.readlines():
      search_replace(f.strip())

if __name__ == '__main__':
  sys.exit(main(sys.argv))
