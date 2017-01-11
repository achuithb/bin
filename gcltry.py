#!/usr/bin/python -tt

import sys
import subprocess
import re

def Test():
  print "Testing"
  exit(0)

def Revision():
  # Get svn info into a string.
  svninfo = subprocess.Popen(['svn', 'info'], stdout=subprocess.PIPE).communicate()[0]
  # Use regex to find the revision.
  revision = re.compile('Revision: (.*)').search(svninfo).group(1)
  return revision

def AddChangelist(args):
  args += [sys.argv[1]]

def AddRevision(args):
  args += ['-r', Revision()]

def AddRietveld(args):
  rietveld = 'chromiumcodereview.appspot.com/' + sys.argv[1]
  args += ['-R', rietveld]

def AddBots(args):
  generic_bots = 'linux_rel,mac_rel,win_rel,linux_asan,linux_clang,android'
  minimal_bots = 'linux_rel'
  chromeos_bots = 'linux_chromeos,linux_chromeos_clang'
  misc_bots = 'cros_x86,linux_chromeos_valgrind'
  bots = minimal_bots + ',' + chromeos_bots
  bots = generic_bots + ',' + chromeos_bots
  bots = chromeos_bots
  args += ['-b', bots]

def AddTitle(args):
  if len(sys.argv) > 2:
    title = sys.argv[2]
  else:
    title = sys.argv[1]
  args += ['--name', title]

def AddClobber(args):
  args += ['-c']

def CreateArgs():
  args = ['gcl', 'try']
  AddChangelist(args)
  AddBots(args)
  AddRevision(args)
  #AddRietveld(args)
  AddClobber(args)
  AddTitle(args)
  return args

def PrintArgs(args):
  argstr = ''
  for a in args:
    if ' ' in a:
      argstr += '"' + a + '"'
    else:
      argstr += a
    argstr += ' '
  print argstr

def Usage():
  exe = sys.argv[0].split('/')[-1]
  print 'Usage: ' + exe + ' <cl name> <patch title>'
  exit(1)

def main():
  #Test()

  if len(sys.argv) < 2:
    print 'Too few args'
    Usage()

  args = CreateArgs()
  PrintArgs(args)

  dryrun = 0;
  if not dryrun:
    subprocess.call(args)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

