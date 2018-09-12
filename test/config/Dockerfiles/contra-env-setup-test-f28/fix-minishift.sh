#!/bin/bash

systemctl start libvirtd || true

/root/minishift-1.23.0-linux-amd64/minishift start -v 5 --profile minishift --disk-size 40gb --memory 8092mb --openshift-version v3.10.0 || /root/minishift-1.23.0-linux-amd64/minishift delete -f

/root/minishift-1.23.0-linux-amd64/minishift delete -f
