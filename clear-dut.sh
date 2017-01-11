#!/bin/sh

stop ui
rm -rf /home/.shadow/* /var/lib/whitelist/* /home/chronos/Local\ State
crossystem clear_tpm_owner_request=1

mount -o remount,rw /

cat >> /etc/chrome_dev.conf
--show-controller-pairing-demo
--show-host-pairing-demo

cryptohome --action=tpm_status
cat > /var/tmp/tpm_password
