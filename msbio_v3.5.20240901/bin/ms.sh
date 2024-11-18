#!/usr/bin/env sh
HOSTUID=`id -u`
HOSTGID=`id -g $UID`
docker run --rm -e HOSTUID=$HOSTUID -e HOSTGID=$HOSTGID -v $PWD/data:/data -v $PWD/license:/license metadocker8/msbio2:latest /msbio/mylib/ms/msbio2.sh $@
docker run --rm -v $PWD/data:/data metadocker8/msbio2:latest chown -R $HOSTUID.$HOSTGID /data

