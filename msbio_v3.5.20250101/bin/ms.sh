#!/usr/bin/env sh
HOSTUID=`id -u`
HOSTGID=`id -g $UID`

rm -rf $PWD/data/logs/*
docker run --rm -v $PWD/data:/data metadocker8/msbio2:latest chown -R $HOSTUID.$HOSTGID /data
docker run --rm -v $PWD/data:/data metadocker8/msbio2:latest chmod -R a+rwx /data
docker run --rm --user=993:989 -e HOSTUID=$HOSTUID -e HOSTGID=$HOSTGID -v $PWD/data:/data -v $PWD/license:/license metadocker8/msbio2:latest /msbio/mylib/ms/msbio2.sh $@
docker run --rm -v $PWD/data:/data metadocker8/msbio2:latest chown -R $HOSTUID.$HOSTGID /data
docker run --rm -v $PWD/data:/data metadocker8/msbio2:latest chmod -R a+rwx /data
