#!/usr/bin/env bash
HOSTUID=`id -u`
HOSTGID=`id -g $UID`
echo "HOSTUID=$HOSTUID"
echo "HOSTGID=$HOSTGID"
NNAME="msbio"
docker network create $NNAME 2>/dev/null
DNAME="msdata"
if [ $# = "0" ]; then
    CNAME="msbio1"
else
    CNAME="msbio$1"
fi
echo "CNAME=$CNAME"
echo "before clean up"
echo "================================================"
docker volume list |grep msdata
echo "================================================"
docker ps -a |grep msbio 
echo "================================================"

docker rm msdata
docker kill $CNAME
docker rm $CNAME
echo "after clean up"
echo "================================================"
docker volume list |grep msdata
echo "================================================"
docker ps -a |grep msbio
echo "================================================"
echo "\n\n"
echo "start volume"
echo "docker run --network=$NNAME --name=$DNAME -v $DNAME:/home/meta_test metadocker8/msdata:latest"
docker run --network=$NNAME --name=$DNAME -v $DNAME:/home/meta_test metadocker8/msdata:latest
echo "================================================"
docker volume list |grep msdata
echo "================================================"
if [ ! -d $PWD/license ]; then
    echo "Are you in the wrong folder? Cannot find: $PWD/license."
    exit 1
fi
docker rm msdata
echo "remove volume container"
echo "================================================"
docker ps -a |grep msdata
echo "================================================"
echo "start container"
echo "docker run -d --network=$NNAME --hostname=$CNAME --name=$CNAME -e HOSTUID=$HOSTUID -e HOSTGID=$HOSTGID -v $DNAME:/home/meta_test -v $PWD/data:/data -v $PWD/license:/license metadocker8/msbio:latest
"
docker run -d --network=$NNAME --hostname=$CNAME --name=$CNAME -e HOSTUID=$HOSTUID -e HOSTGID=$HOSTGID -v $DNAME:/home/meta_test -v $PWD/data:/data -v $PWD/license:/license metadocker8/msbio:latest
echo "================================================"
docker ps -a |grep msbio
echo "================================================"
echo "To delete containers later, use bin/debug_down.sh"
