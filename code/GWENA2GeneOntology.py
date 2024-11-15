
#Conda env name: gwenav2


import pandas as pd
import numpy as np
import docker
import argparse
import subprocess
import os

parser = argparse.ArgumentParser(description='GWENA2GeneOntology')

parser.add_argument('--gwena_enrichment_file', type=str, help='Input file path')
parser.add_argument('--output_directory', type=str, help='Output directory path')
parser.add_argument('--go_figure_download_location', type=str, help='Docker image name')

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
    sample_sheet = pd.DataFrame('module' = module, 'go_pathway' = go_pathway)
    return sample_sheet

def seperate_module_genes(sample_sheet, output_directory):
    module_files = []
    for i in pd.sample_sheet['module'].unique():
        module = sample_sheet[sample_sheet['module'] == i]
        module_file = os.path.join(output_directory, f"module_{i}_gene_list.csv")
        module.to_csv(f"{output_directory}/module_gene_list/module_{i}_gene_list.csv", sep="\t", index=False)
        module_files.append(module_file)
    return module_files


def metascape_docker_run(module_gene_list, output_directory):
    """
    Run Metascape docker container to pefom gene metascape comparison
    https://metascape.org/gp/index.html#/menu/msbio

    Metascape Docker file must be downloaded with authentication from Metascape website.

    Example for single-gene-list analysis:
    bin/ms.sh -u -o /data/output_single_id_txt /data/example/single_list_id.txt

    """
    try:
        client = docker.from_env()
        client.containers.run(image_name, f"bin/ms.sh -u -o {output_directory}/metascape /data/example/single_list_id.txt", remove=True)
        
    except Exception as e:
        print(f"Error: {e}")
    
def GoFigure_run(module_gene_list, output_directory, go_figure_download_location):
    """
    Run GoFigure to perform gene ontology analysis
    """
    command = [
    "python3",
    "/Users/bigyambat/miniforge3/pkgs/go-figure-1.0.2-hdfd78af_0/python-scripts/gofigure.py",
    "-i", module_gene_list,
    "-o", "f{output_directory}/GoFigure",
    ]

    try:
        GoFigure_Command = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        print(f"Error: {e}")

def main():

    if not os.path.exists(args.output_directory):
        os.path.makedirs(args.output_directory)

    #Creating Sample Sheet
    sample_sheet = create_gene_list(args.gwena_enrichment_file)

    module_gene_files = seperate_module_genes(sample_sheet, args.output_directory)

    for module_gene_file in module_gene_files:
        print(f"Running Metascape and GoFigure for {module_gene_file}")
        metascape_docker_run(module_gene_file, args.output_directory)
        GoFigure_run(module_gene_file, args.output_directory, args.go_figure_download_location)

if __name__ == "__main__":
    main()