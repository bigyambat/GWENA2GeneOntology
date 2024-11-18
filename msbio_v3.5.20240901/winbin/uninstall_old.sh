@echo off
# we now uses msbio.oraclelinux8 instead of msbio.centos8
# this script is to help you identify and remove msbio.centos8 image to save disk space
echo "Step 1. If you see containers in any of the output below, run 'docker kill [container_id]' then 'docker rm [container_id]'"
docker container ls --all --filter=ancestor=metadocker8/msbio:centos8 --format "table {{.ID}}\t{{.Image}}" 
docker container ls --all --filter=ancestor=metadocker8/msbio:oraclelinux8 --format "table {{.ID}}\t{{.Image}}" 
docker container ls --all --filter=ancestor=metadocker8/msdata:centos8 --format "table {{.ID}}\t{{.Image}}"
docker container ls --all --filter=ancestor=metadocker8/msdata:oraclelinux8 --format "table {{.ID}}\t{{.Image}}"
echo .
echo "Step 2. Run the following to remove obsolete images:"
echo "    docker rmi -f metadocker8/msbio:centos8"
echo "    docker rmi -f metadocker8/msbio:oraclelinux8"
echo "    docker rmi -f metadocker8/msdata:centos8"
echo "    docker rmi -f metadocker8/msdata:oraclelinux8"
echo .
