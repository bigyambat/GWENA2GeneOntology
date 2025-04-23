@echo off
docker run --rm -it -v %CD%\data:/data -v %CD%\license:/license metadocker8/msbio2:latest /bin/bash
