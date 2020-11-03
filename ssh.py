#!/usr/bin/python

import argparse
import os
import sys

import constants
import utils

def IsVM(opts):
  return opts.vm or (opts.port != constants.VM_PORT)


def Deploy(opts, host):
  cmd = ['deploy_chrome', '--force',
         '--build-dir=out_%s/Release' % os.environ['SDK_BOARD']]

  if opts.nostrip:
    cmd += ['--mount', '--nostrip']

  if IsVM(opts):
    cmd += ['--to=localhost', '--port=%s' % opts.port]
  else:
    cmd += ['--to=%s' % host]

  utils.RunCmd(cmd, call=True)

def ForwardPorts(opts):
  forward_port = None
  flag = None
  if opts.forward_port:
    forward_port = opts.forward_port
    forward_flag = '-L'
  if opts.remote_port_forward:
    forward_port = opts.remote_port_forward
    forward_flag = '-R'
  if forward_port:
    return [forward_flag, '%d:localhost:%d' % (forward_port, forward_port)]
  return []

def Remote(opts, host, src, dest):
  cmd = ['scp'] if opts.scp else ['ssh']
  cmd += ['-o', 'UserKnownHostsFile=/dev/null', '-o',
          'StrictHostKeyChecking=no', '-i',
          os.path.join(utils.CHROME_DIR,
                       'third_party/chromite/ssh_keys/testing_rsa')]
  cmd += ForwardPorts(opts)

  if IsVM(opts):
    port_flag = '-P' if opts.scp else '-p'
    cmd += [port_flag, opts.port]
    remote = 'root@localhost'
  else:
    remote = 'root@%s' % host
  if src:
    cmd += [src]
  if dest:
    remote += ':' + dest
  cmd += [remote]

  utils.RunCmd(cmd, call=True)


def CreateParser():
  parser = argparse.ArgumentParser('Script for SSH/SCP/Deploy')
  parser.add_argument('--forward-port', '-L', type=int, help='Port to forward')
  parser.add_argument('--remote-port-forward', '-R', type=int,
                      help='Remote port to forward')
  parser.add_argument('--vm', action='store_true', default=False,
                      help='SSH into VM')
  parser.add_argument('--port', '-p', default=constants.VM_PORT,
                      help='VM port (default %s)' % constants.VM_PORT)
  parser.add_argument('--dut', action='store_true', default=False,
                      help='SSH into DUT')
  parser.add_argument('--scp', action='store_true', default=False,
                      help='SCP instead of SSH')
  parser.add_argument('--deploy', action='store_true', default=False,
                      help='deploy_chrome instead of SSH')
  parser.add_argument('--nostrip', action='store_true', default=False,
                      help='use nostrip with deploy_chrome')
  return parser


def main(argv):
  opts, rem = utils.ParseArgs(CreateParser(), argv, allow_rem=True)

  src = None
  dest = None
  host = constants.DEVICE_IP
  if opts.scp:
    assert(len(rem) == 2), 'scp must have 2 args'
    src = rem[0]
    dest = rem[1]
  elif rem:
    host = rem[0]
  if opts.deploy:
    Deploy(opts, host)
  else:
    Remote(opts, host, src, dest)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
