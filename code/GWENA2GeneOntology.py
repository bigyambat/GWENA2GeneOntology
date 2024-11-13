
#Conda env name: gwenav2


import pandas as pd
import numpy as np
import docker

#Install the following packages
#pip install pandas
#pip install numpy
#pip install docker

def create_gene_list(input_file):


def metascape_docker_run(image_name, output_):
    """
    Run Metascape docker container for 
    https://metascape.org/gp/index.html#/menu/msbio

    Example for single-gene-list analysis:
    bin/ms.sh -u -o /data/output_single_id_txt /data/example/single_list_id.txt

    """
    try:
        client = docker.from_env()
        client.containers.run(image_name, f"bin/ms.sh -u -o /data/output_single_id_txt /data/example/single_list_id.txt", remove=True)

    client = docker.from_env()
    except Exception as e:
        print(f"Error: {e}")