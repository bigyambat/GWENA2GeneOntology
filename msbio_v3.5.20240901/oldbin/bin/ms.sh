#!/usr/bin/env bash
# when run .job, there may be no - arguments.
# OSX doesnot support \+ in sed
if [[ $1 =~ [0-9][0-9]* ]]; then
    CNAME="msbio$1"
    PARAM=`echo $@ | sed 's/[0-9][0-9]*//'`
else
    CNAME="msbio1"
    PARAM=$@
fi
docker exec -w /home/meta_test $CNAME /home/meta_test/mylib/ms/msbio.py --license=/license $PARAM
