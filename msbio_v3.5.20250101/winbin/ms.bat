:: when run .job, there may be no - arguments.
@echo off
docker run --rm -v %CD%\data:/data -v %CD%\license:/license metadocker8/msbio2:latest /msbio/mylib/ms/msbio2.sh %*
