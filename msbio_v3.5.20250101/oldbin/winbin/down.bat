@echo off
SET DNAME=msdata
SET NNAME=msbio
if [%1]==[] (
    SET CNAME=msbio1
) else (
    SET CNAME=msbio%1
)
if "%CNAME%" == "msbio1" (
:: ^ used to escape
    for /f "usebackq" %%a in (`docker ps -a --filter volume^=%DNAME% ^|find /c /v ""`) do (
        if %%a geq 3 (
            echo Cannot shutdown %CNAME%, as other containers need its MySQL server!
            exit 0
        )
    )
) 
docker kill %CNAME% 2>NUL
docker volume rm %DNAME% 2>NUL
docker network rm %NNAME% 2>NUL

