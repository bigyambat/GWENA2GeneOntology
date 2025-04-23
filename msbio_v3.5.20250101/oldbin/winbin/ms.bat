:: when run .job, there may be no - arguments.
@echo off
:: https://stackoverflow.com/questions/25306909/how-to-check-a-string-does-not-start-with-a-number-in-batch
setlocal EnableDelayedExpansion
set digits=0123456789
set var=%1
if "!digits:%var:~0,1%=!" neq "%digits%" (
::    First char is digit
    SET CNAME=msbio%1
:: https://stackoverflow.com/questions/935609/batch-parameters-everything-after-1
    for /f "tokens=1,* delims= " %%a in ("%*") do set PARAM=%%b
) else (
::    First char is not digit
    SET CNAME=msbio1
    SET PARAM=%*
)
docker exec -w /home/meta_test %CNAME% /home/meta_test/mylib/ms/msbio.py --license=/license %PARAM%
