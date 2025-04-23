#!/usr/bin/env sh
#HOSTUID=`id -u`
#HOSTGID=`id -g $UID`
#docker run --rm -it --name=msone_debug -e HOSTUID=$HOSTUID -e HOSTGID=$HOSTGID -v $PWD/data:/data -v $PWD/license:/license metadocker8/msone:latest /bin/bash
docker run --rm -it --user $HOSTUID:$HOSTGID --name=msone_debug -v $PWD/data:/data -v $PWD/license:/license metadocker8/msbio2:latest /bin/bash
