#!/usr/bin/python

import re

def grep(constant):
  py_files = ['auth_server.py',
              'auth_server_unittest.py',
              'httpd.py',
              'httpd_unittest.py']
  for py_file in py_files:
    if constant in open(py_file, 'r').read():
      return True
  return False

used_constants = []
unused_constants = []
with open('constants.py', 'r') as f:
  for line in f:
    m = re.search(r"^[A-Z0-9_]+", line)
    if m:
      c = m.group(0)
      if grep(c):
        used_constants.append(c)
      else:
        unused_constants.append(c)

print "Used constants:"
print used_constants
print "Unused constants:"
print unused_constants

