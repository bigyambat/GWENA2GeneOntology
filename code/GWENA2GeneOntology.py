
#Conda env name: gwenav2


import pandas as pd
import numpy as np
import docker
import argparse

parser = argparse.ArgumentParser(description='GWENA2GeneOntology')

parser.add_argument('--gwena_enrichment_file', type=str, help='Input file path')
parser.add_argument('--output_directory', type=str, help='Output directory path')

#Parse Arguments
args = parser.parse_args()

#Install the following packages
#pip install pandas
#pip install numpy
#pip install docker

def create_gene_list(input_file):
    enrichment_data = pd.read_excel(input_file, header=None)
    module = enrichment_data.iloc[:, 0]
    go_pathway = enrichment_data.iloc[:, 5]

    sample_sheet = pd.create_data_frame(module, go_pathway)

    return sample_sheet

def seperate_module_genes(sample_sheet):
    for i in range(len(unique(sample_sheet['module']))):
        module = sample_sheet[sample_sheet['module'] == i]
        module.to_tsv(f"module_gene_list{i}.tsv")
    return 


def metascape_docker_run(image_name, output_directory):
    """
    Run Metascape docker container for 
    https://metascape.org/gp/index.html#/menu/msbio

    Metascape Docker file must be downloaded with authentication from Metascape website.

    Example for single-gene-list analysis:
    bin/ms.sh -u -o /data/output_single_id_txt /data/example/single_list_id.txt

    """
    try:
        client = docker.from_env()
        client.containers.run(image_name, f"bin/ms.sh -u -o /data/output_single_id_txt /data/example/single_list_id.txt", remove=True)
        
    except Exception as e:
        print(f"Error: {e}")
    

def main():
    print("Hello World!")


if __name__ == "__main__":
    main()