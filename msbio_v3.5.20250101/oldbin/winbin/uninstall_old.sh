@echo off
# we now uses msbio.oraclelinux8 instead of msbio.centos8
# this script is to help you identify and remove msbio.centos8 image to save disk space
echo "Step 1. If you see containers in the output below, run 'docker kill [container_id]' then 'docker rm [container_id]'"
docker container ls --all --filter=ancestor=metadocker8/msbio:centos8 --format "table {{.ID}}\t{{.Image}}" 
echo .
echo "Step 2. If you see containers in the output below, run 'docker kill [container_id]' then 'docker rm [container_id]'"
docker container ls --all --filter=ancestor=metadocker8/msdata:centos8 --format "table {{.ID}}\t{{.Image}}"
echo.
echo "Step 3. Run the following to remove obsolete images:"
echo "    docker rmi metadocker8/msbio:centos8"
echo "    docker rmi metadocker8/msdata:centos8"
echo.
