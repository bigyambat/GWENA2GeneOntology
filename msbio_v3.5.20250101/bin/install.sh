#!/usr/bin/env bash
docker pull metadocker8/msbio2:latest
if [ ! -d "data" ]
then
    mkdir data
fi
chmod a+rwx data
if [ ! -d "data/logs" ]
then
    mkdir data/logs
fi
chmod a+rwx data/logs

