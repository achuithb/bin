#!/usr/bin/python

import os

import utils


WORKING_DIRS = [
    os.path.join(utils.CROS_DIR, w) for w in [
        'chromite',
        'docs',
        'src/third_party/chromiumos-overlay',
        # 'src/platform2',
        # 'src/platform/dev',
        # 'src/private-overlays/overlay-amd64-generic-cheets-private',
        # 'src/private-overlays/overlay-betty-private',
        # 'src/third_party/autotest/files',
        # 'src/third_party/autotest-private',
    ]
]

CHROMITE_FILES = [
    'lib/vm.py',
    'cli/cros/cros_chrome_sdk.py',
    'cli/cros/cros_flash.py',
    'cli/flash.py',
    # 'lib/cros_build_lib.py',
    # 'lib/dev_server_wrapper.py',
    # 'lib/path_util.py',
    # 'lib/gs.py',
    # 'lib/cros_test.py',
    # 'lib/cros_test_unittest.py',
    # 'lib/paygen/paygen_payload_lib.py',
    'scripts/deploy_chrome.py',
    # 'lib/constants.py',
    # 'lib/chrome_util.py',
    # 'lib/remote_access.py',

    # Nebraska.
    # 'lib/auto_updater.py',
    # 'lib/auto_updater_transfer.py',
    # 'lib/nebraska_wrapper.py',

    # XBuddy.
    # 'lib/xbuddy/build_artifact.py',
    # 'lib/xbuddy/common_util.py',
    # 'lib/xbuddy/downloader.py',
    # 'lib/xbuddy/xbuddy.py',
]
