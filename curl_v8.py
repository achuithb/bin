#!/usr/bin/python

import sys

import git_lib, utils


DIFF_FILE = '/tmp/curl_v8.diff'


def CurlV8(url):
  diff_file = '/tmp/curl_v8.diff'
  tmp_file = '/tmp/curl_v8_64.diff'
  utils.RunCmd(['curl', url, '-o', tmp_file])
  with open(diff_file, 'w')  as f:
    f.write(utils.RunCmd(['base64', '--decode', tmp_file], silent=True))
  utils.RunCmd(['rm', '-f', tmp_file])
  return diff_file


def Usage(argv):
  print 'Usage: %s <url>' % argv[0].split('/')[-1]
  sys.exit(1)


def main(argv):
  if len(argv) < 2:
    Usage(argv)

  diff_file = CurlV8(argv[1])
  git_lib.GitApply(diff_file)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
