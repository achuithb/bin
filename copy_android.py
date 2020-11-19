#!/usr/bin/python

import argparse
import os
import shutil
import sys

import utils


def CopyAndroid(target_dir, dry_run):
  target_device ='cheets_x86'
  target_host ='linux-x86'
  android_product_out = os.path.join(
      utils.ANDROID_DIR, 'out/target/product', target_device)
  android_dist_out = os.path.join(
      utils.ANDROID_DIR, 'out/dist')
  android_host_out = os.path.join(
      utils.ANDROID_DIR, 'out/host', target_host)

  cros_android_path = target_dir or os.path.join(
      utils.CROS_DIR, 'src/private-overlays/project-cheets-private',
      'chromeos-base/android-container-pi/files')

  def Copy(path):
    utils.ColorPrint(utils.BLUE, 'cp %s->%s' % (path, cros_android_path))
    if not dry_run:
      shutil.copy(path, cros_android_path)

  utils.ColorPrint(utils.RED, 'rmtree ' + cros_android_path)
  utils.ColorPrint(utils.CYAN, 'mkdir -p ' + cros_android_path)
  if not dry_run:
    shutil.rmtree(cros_android_path, ignore_errors=True)
    os.makedirs(cros_android_path)

  Copy(os.path.join(android_product_out, 'system.img'))
  Copy(os.path.join(android_product_out, 'vendor.img'))
  Copy(os.path.join(android_product_out, 'root', 'plat_file_contexts'))
  Copy(os.path.join(android_product_out, 'root', 'vendor_file_contexts'))
  Copy(os.path.join(android_dist_out, 'sepolicy.zip'))
  Copy(os.path.join(android_dist_out, 'XkbToKcmConverter'))
  Copy(os.path.join(android_host_out,
                    'framework/org.chromium.arc.cachebuilder.jar'))

  utils.RunCmd('ls -ltF ' + cros_android_path)


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Copy android files to chromeos build')
  parser.add_argument('--target-dir', help='Target directory')
  return utils.ParseArgs(parser, argv)


def main(argv):
  utils.AssertCWD(utils.ANDROID_DIR)
  opts = ParseArgs(argv)
  CopyAndroid(opts.target_dir, opts.dry_run)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
