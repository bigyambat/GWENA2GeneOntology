@echo off
SET DNAME=msdata
SET NNAME=msbio
docker network create %NNAME% 2>NUL
if [%1]==[] (
    SET CNAME=msbio1
) else (
    SET CNAME=msbio%1
)
docker kill %CNAME% 2>NUL
docker run --rm --network=%NNAME% --name=%DNAME% -v %DNAME%:/home/meta_test metadocker8/msdata:latest
docker run --rm -d --network=%NNAME% --hostname=%CNAME% --name=%CNAME% -v %DNAME%:/home/meta_test -v %CD%\data:/data -v %CD%\license:/license metadocker8/msbio:latest
