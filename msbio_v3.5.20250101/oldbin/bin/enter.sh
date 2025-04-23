#!/usr/bin/env bash
if [ $# = "0" ]; then
    CNAME="msbio1"
else
    CNAME="msbio$1"
fi
docker exec -it $CNAME /bin/bash
