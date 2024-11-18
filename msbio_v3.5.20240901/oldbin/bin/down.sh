#!/usr/bin/env bash
DNAME="msdata"
NNAME="msbio"
if [ $# = "0" ]; then
    CNAME="msbio1"
else
    CNAME="msbio$1"
fi
if [ $CNAME = "msbio1" ]; then
    n=`docker ps -a --filter volume=$DNAME | wc -l`
    if (($n > 2)); then
        echo "Cannot shutdown $CNAME, as other containers need its MySQL server!"
        exit 0
    fi
fi
docker kill $CNAME 2>/dev/null
docker volume rm $DNAME 2>/dev/null
docker network rm $NNAME 2>/dev/null
