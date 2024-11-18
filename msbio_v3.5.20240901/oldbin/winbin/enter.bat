@echo off
if [%1]==[] (
    SET CNAME=msbio1
) else (
    SET CNAME=msbio%1
)
docker exec -it %CNAME% /bin/bash
