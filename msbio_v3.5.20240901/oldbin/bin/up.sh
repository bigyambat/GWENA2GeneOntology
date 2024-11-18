#!/usr/bin/env bash
HOSTUID=`id -u`
HOSTGID=`id -g $UID`
NNAME="msbio"
docker network create $NNAME 2>/dev/null
DNAME="msdata"
if [ $# = "0" ]; then
    CNAME="msbio1"
else
    CNAME="msbio$1"
fi
docker kill $CNAME 2>/dev/null
docker run --rm  --network=$NNAME --name=$DNAME -v $DNAME:/home/meta_test metadocker8/msdata:latest
if [ ! -d $PWD/license ]; then
    echo "Are you in the wrong folder? Cannot find: $PWD/license."
    exit 1
fi
docker run --rm -d --network=$NNAME --hostname=$CNAME --name=$CNAME -e HOSTUID=$HOSTUID -e HOSTGID=$HOSTGID -v $DNAME:/home/meta_test -v $PWD/data:/data -v $PWD/license:/license metadocker8/msbio:latest
