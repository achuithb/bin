#!/usr/bin/python

import argparse
import subprocess
import sys
import os

import constants

HOME = os.environ['HOME']
BOARD = 'amd64-generic'
dryrun = 0


def LocalPath(path):
  return os.path.realpath(os.path.join(HOME, path))

def LocalCrosPath(path):
  return os.path.join(LocalPath('code/cros'), path)


# Desktop -> DUT.
# TODO: Move to cros_paths
DIRECTORY_MAPPINGS = {
    '/tmp' : '/tmp',
    '/var/tmp' : '/var/tmp',
    LocalPath('code/misc/logs') : '/var/log/chrome',
    LocalPath('Downloads') : '/home/chronos/user/Downloads',
    LocalPath('code/chrome/src') : '/usr/local/telemetry/src',
    LocalPath('code/catapult') :
        '/usr/local/telemetry/src/third_party/catapult',
    LocalCrosPath('src/third_party/autotest/files/client') :
        '/usr/local/autotest',
    LocalCrosPath('src/third_party/autotest-tests-cheets/client/site_tests') :
        '/usr/local/autotest/tests',
    LocalCrosPath('src/third_party/autotest-private/client/site_tests') :
        '/usr/local/autotest/tests',
    LocalCrosPath('src/third_party/autotest/files/client/site_tests') :
        '/usr/local/autotest/tests',
    LocalCrosPath(os.path.join('chroot/build', BOARD,
                               'usr/local/build/autotest/client')) :
        '/usr/local/autotest',
    LocalCrosPath(os.path.join('chroot/build', BOARD,
                               'usr/local/build/autotest/client/site_tests')) :
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


def CleanupPyc(dirname):
  RunCmd(['find', dirname, '-name', '*.pyc', '-delete'])


def TarDir(dirname):
  CleanupPyc(dirname)

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


def TransferFile(filename, host, port, reverse):
  src_path = os.path.abspath(filename)
  if not os.path.exists(src_path) and not reverse:
    raise Exception('File does not exist %s' % filename)

  tarred = False
  if os.path.isdir(src_path):
    if reverse:
      raise Exception('Cannot fetch a remote directory %s' % filename)
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


def GetHost(args):
  if args.host:
    return args.host
  if args.vm:
    return constants.VM_IP
  if args.dut:
    return constants.DEVICE_IP
  return constants.VM_IP


def GetPort(args):
  if args.host or args.dut:
    return None
  if args.port:
    return args.port
  if args.vm:
    return constants.VM_PORT
  return constants.VM_PORT


def TransferFiles(args):
  global dryrun
  dryrun = args.dryrun

  host = GetHost(args)
  port = GetPort(args)
  for filename in args.files:
    TransferFile(filename, host, port, args.reverse)


def Parse():
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', dest='host', help='hostname to connect to')
  parser.add_argument('files', help='files to transfer', nargs='*')
  parser.add_argument('-p', '--port', dest='port',
                      help='port (default %s)' % constants.VM_PORT)
  parser.add_argument('--vm', action='store_true')
  parser.add_argument('--dut', action='store_true',
                      help='%s' % constants.DEVICE_IP)
  parser.add_argument('-r', '--reverse', action='store_true')
  parser.add_argument('-d', '--dryrun', action='store_true')
  return parser.parse_args()


def main(argv):
  TransferFiles(Parse())


if __name__ == '__main__':
  sys.exit(main(sys.argv))
