#!/usr/bin/env bash
# when run .job, there may be no - arguments.
if [[ $1 =~ [0-9][0-9]* ]]; then
    CNAME="msbio$1"
    PARAM=`echo $@ | sed 's/[0-9][0-9]*//'`
else
    CNAME="msbio1"
    PARAM=$@
fi
echo "CNAME=$CNAME"
echo "PARAM=$PARAM"
echo "before start"
echo "================================================"
docker ps -a |grep msbio
echo "================================================"
docker volume ls |grep msdata
echo "================================================"
echo "docker exec -w /home/meta_test $CNAME /home/meta_test/mylib/ms/msbio.py --license=/license $PARAM"
docker exec -w /home/meta_test $CNAME /home/meta_test/mylib/ms/msbio.py --license=/license $PARAM
