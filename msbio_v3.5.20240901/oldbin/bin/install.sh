#!/usr/bin/env bash
docker pull metadocker8/msbio:latest
docker pull metadocker8/msdata:latest
if [ ! -d "data" ]
then
    mkdir data
fi
chmod a+rwx data
