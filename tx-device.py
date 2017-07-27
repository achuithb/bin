#!/usr/bin/python

import argparse
import subprocess
import sys
import os

DEVICE_IP='100.96.59.85'
ALT_DEVICE_IP='100.96.56.235'
VM_IP='localhost'
VM_PORT='9222'
HOME = os.environ['HOME']
CHROME_DIR = os.path.join(HOME, 'code/chrome/src')
CROS_DIR = os.path.join(HOME, 'code/cros')
CATAPULT_DIR = os.path.join(HOME, 'code/catapult')
BOARD = 'wolf'

dryrun = 0

DIRECTORY_MAPPINGS = {
    '/tmp' : '/tmp',
    '/var/tmp' : '/var/tmp',
    os.path.join(HOME, 'Downloads') : '/home/chronos/user/Downloads',
    CHROME_DIR : '/usr/local/telemetry/src',
    CATAPULT_DIR : '/usr/local/telemetry/src/third_party/catapult',
    os.path.join(CROS_DIR,
                 'src/third_party/autotest/files/client') :
                     '/usr/local/autotest',
    os.path.join(CROS_DIR,
                 'src/third_party/autotest-tests-cheets/client/site_tests') :
                     '/usr/local/autotest/tests',
    os.path.join(CROS_DIR,
                 'src/third_party/autotest-private/client/site_tests') :
                     '/usr/local/autotest/tests',
    os.path.join(CROS_DIR,
                 'src/third_party/autotest/files/client/site_tests') :
                     '/usr/local/autotest/tests',
    os.path.join(CROS_DIR, 'chroot/build', BOARD,
                 'usr/local/build/autotest/client/site_tests') :
                     '/usr/local/autotest/tests',
}


def RunCmd(cmd):
  print (' ').join(cmd)
  if not dryrun:
    subprocess.call(cmd)


def SshArgs():
  return ['-o', 'UserKnownHostsFile=/dev/null',
         '-o', 'StrictHostKeyChecking=no', '-i',
         '%s/code/chrome/src/third_party/chromite/ssh_keys/testing_rsa' % HOME]


def Ssh(host, port, cmd):
  ssh  = ['ssh'] + SshArgs()
  if port:
    ssh += ['-p', port]
  ssh += ['root@%s' % host, '-C']
  if not isinstance(cmd, list):
    cmd = cmd.split()
  ssh.extend(cmd)
  RunCmd(ssh)


def Scp(paths, port):
  scp = ['scp'] + SshArgs()
  if port:
    scp += ['-P', port]
  scp.extend(paths)
  RunCmd(scp)


def TarDir(dirname):
  tar_file = dirname + '.tar'
  tar_cmd = ['tar', 'cvzf', tar_file,
             '--exclude="\*\.pyc"', '--exclude=\*\.svn', '--exclude=\*\.git',
             dirname]
  RunCmd(tar_cmd)
  return tar_file


def UnTar(host, port, dest_path, strip):
  cwd = os.path.dirname(dest_path)
  tar_file = os.path.basename(dest_path)
  tar_dir = os.path.splitext(tar_file)[0]
  untar_cmd = (
      'cd %s; '
      'rm -rf %s; '
      'tar xvzf %s --strip-components %d; '
      'rm -f %s; '
      'chown -R chronos:chronos %s'
      % (cwd, tar_dir, tar_file, strip, tar_file, tar_dir))
  Ssh(host, port, untar_cmd)


def DestPath(src_path):
  match = None
  for src_prefix, dest_prefix in DIRECTORY_MAPPINGS.iteritems():
    if src_path.startswith(src_prefix):
      print "Matched " + src_prefix
      if match is None or src_prefix.startswith(match['src_prefix']):
        match = {'src_prefix': src_prefix, 'dest_prefix': dest_prefix}
  if not match:
    raise Exception('%s not in directory mapping' % src_path)
  print "Best match " + match['src_prefix']
  rel_path = src_path[len(match['src_prefix']):]
  return "%s%s" % (match['dest_prefix'], rel_path)


def TransferFile(file, host, port, reverse):
  src_path = os.path.abspath(file)
  if not os.path.exists(src_path) and not reverse:
    raise Exception('File does not exist %s' % file)

  tarred = False
  if os.path.isdir(src_path):
    if reverse:
      raise Exception('Cannot fetch a remote directory %s' % file)
    tarred = True
    src_path = TarDir(src_path)

  dest_path = DestPath(src_path)
  dest_addr = 'root@%s:%s' % (host, dest_path)
  paths = [src_path, dest_addr]
  if reverse:
    paths = reversed(paths)

  Ssh(host, port, ['mkdir', '-p', os.path.dirname(dest_path)])
  Scp(paths, port)
  if tarred:
    UnTar(host, port, dest_path, src_path.count('/') - 1)
    if not dryrun:
      os.remove(src_path)


def GetHostFromArgs(args):
  if args.host:
    return args.host
  if args.vm:
    return VM_IP
  if args.device:
    return DEVICE_IP
  if args.alt_device:
    return ALT_DEVICE_IP
  return DEVICE_IP


def GetPortFromArgs(args):
  if args.port:
    return args.port
  if args.vm:
    return VM_PORT
  return args.port


def TransferFiles(args):
  global dryrun
  dryrun = args.dryrun

  host = GetHostFromArgs(args)
  port = GetPortFromArgs(args)
  for file in args.files:
    TransferFile(file, host, port, args.reverse)


def Parse():
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', dest='host', help='hostname to connect to')
  parser.add_argument('files', help='files to transfer', nargs='*')
  parser.add_argument('-p', '--port', dest='port', help='port')
  parser.add_argument('--vm', action='store_true')
  parser.add_argument('--device', action='store_true', help='%s' % DEVICE_IP)
  parser.add_argument('--alt-device', action='store_true',
                      help='%s' % ALT_DEVICE_IP)
  parser.add_argument('-r', '--reverse', action='store_true')
  parser.add_argument('-d', '--dryrun', action='store_true')
  return parser.parse_args()


def main(argv):
  TransferFiles(Parse())


if __name__ == '__main__':
  sys.exit(main(sys.argv))
