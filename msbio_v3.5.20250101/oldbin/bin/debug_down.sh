#!/usr/bin/env bash
DNAME="msdata"
NNAME="msbio"
if [ $# = "0" ]; then
    CNAME="msbio1"
else
    CNAME="msbio$1"
fi
echo "CNAME=$CNAME"
if [ $CNAME = "msbio1" ]; then
    n=`docker ps -a --filter volume=$DNAME | wc -l`
    if (($n > 2)); then
        echo "Cannot shutdown $CNAME, as other containers need its MySQL server!"
        exit 0
    fi
fi
echo "before kill container"
echo "================================================"
docker ps -a |grep msbio
echo "================================================"
echo "docker kill $CNAME"
docker kill $CNAME
echo "after kill container"
echo "================================================"
docker ps -a |grep msbio
echo "================================================"
echo "before remove volume"
echo "================================================"
docker volume ls |grep msdata
echo "================================================"
docker rm $CNAME
echo "after kill container"
echo "================================================"
docker ps -a |grep msbio
echo "================================================"
echo "docker volume rm $DNAME"
docker volume rm $DNAME
echo "after remove volume"
echo "================================================"
docker volume ls |grep msdata
echo "================================================"
echo "docker network rm $NNAME"
docker network rm $NNAME
