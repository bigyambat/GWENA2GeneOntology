#!/usr/bin/env bash
HOSTUID=$UID
HOSTGID=`id -g $UID`
CNAME="msbio1"
docker exec -it $CNAME chown -R $HOSTUID.$HOSTGID $@

