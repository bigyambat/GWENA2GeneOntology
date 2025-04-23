#!/usr/bin/env sh
HOSTUID=$UID
HOSTGID=`id -g $UID`
docker run --rm -v $PWD/data:/data metadocker8/msone:latest chown -R $HOSTUID.$HOSTGID $@
