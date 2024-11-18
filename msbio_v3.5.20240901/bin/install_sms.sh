#!/usr/bin/env bash
singularity build --force msbio2.sif docker://metadocker8/msbio2:latest
if [ ! -d "data" ]
then
    mkdir data
fi
chmod a+rwx data
