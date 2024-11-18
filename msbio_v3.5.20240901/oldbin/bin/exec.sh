#!/usr/bin/env bash
# when run .job, there may be no - arguments.
# OSX doesnot support \+ in sed
CNAME="msbio1"
PARAM=$@
docker exec -w /home/meta_test $CNAME $@
