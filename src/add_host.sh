#!/bin/bash
echo "172.19.103.251 bcpmiddlewaredev.bangchak.co.th" >> /etc/hosts
echo "172.19.103.160 bcpmiddlewareprod.bangchak.co.th" >> /etc/hosts
exec "$@"
