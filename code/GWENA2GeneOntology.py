
#Conda env name: gwenav2

#Install the following packages
#pip install pandas
#pip install numpy
#pip install docker

# Command Line Usage:
# python GWENA2GeneOntology.py --gwena_enrichment_file /path/to/gwena_enrichment_file.xlsx --output_directory /path/to/output_directory --metascape_download_location /path/to/metascape_download_location

# Test Run
# /Users/bigyambat/Desktop/GWENA2GeneOntology/code/GWENA2GeneOntology.py --gwena_enrichment_file /Users/bigyambat/Desktop/GWENA2GeneOntology/test_data/Enrichment_Complete.xlsx --output_directory /Users/bigyambat/Desktop/GWENA2GeneOntology/test_data --metascape_download_location /Users/bigyambat/Desktop/GWENA2GeneOntology/msbio_v3.5.20240901

import pandas as pd
import numpy as np
import docker
import argparse
import subprocess
import os

#Create option parser
parser = argparse.ArgumentParser(description='GWENA2GeneOntology')
parser.add_argument('--gwena_enrichment_file', type=str, help='Input file path')
parser.add_argument('--output_directory', type=str, help='Output directory path')
parser.add_argument('--metascape_download_location_download_location', type=str, help='Metascape Docker image file location')

#Parse Arguments
args = parser.parse_args()

def create_gene_list(input_file):
    enrichment_data = pd.read_excel(input_file, header=None)
    module = enrichment_data.iloc[:, 0]
    go_pathway = enrichment_data.iloc[:, 5]
    go_pathway = go_pathway[go_pathway.str.startswith("GO:", na=False)]
    sample_sheet = pd.DataFrame({'module': module, 'go_pathway': go_pathway})
    return sample_sheet

def seperate_module_genes(sample_sheet, output_directory):
    module_files = []
    module_path = os.path.join(output_directory, "module_gene_list")
    os.makedirs(module_path, exist_ok=True)
    for i in pd.sample_sheet['module'].unique():
        module = sample_sheet[sample_sheet['module'] == i]
        file_path = os.path.join(module_path, f"module_{i}_gene_list.csv")
        module.to_csv(file_path, sep="\t", index=False)
        module_files.append(module_file)
    return module_files


def metascape_docker_run(module_gene_list, output_directory, metascape_download_location):
    """
    Run Metascape docker container to pefom gene metascape comparison
    https://metascape.org/gp/index.html#/menu/msbio

    Metascape Docker file must be downloaded with authentication from Metascape website.

    Example for single-gene-list analysis:
    bin/ms.sh -u -o /data/output_single_id_txt /data/example/single_list_id.txt

    """
    try:
        client = docker.from_env()
        client.containers.run(args.go_figure_download_location, f"{args.go_figure_download_location}/bin/ms.sh -u -o {output_directory}/metascape {module_gene_list}", remove=True)
        
    except Exception as e:
        print(f"Error: {e}")
    
def GoFigure_run(module_gene_list, output_directory):
    """
    Run GoFigure! to perform gene ontology analysis on module gene list
    """

    #Filtering out non-GO pathways
    module_gene_list = module_gene_list[module_gene_list.str.startswith("GO:", na=False)]

    command = [
    "python3",
    "/Users/bigyambat/miniforge3/pkgs/go-figure-1.0.2-hdfd78af_0/python-scripts/gofigure.py",
    "-i", module_gene_list,
    "-o", f"{output_directory}/GoFigure",
    ]

    try:
        GoFigure_Command = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        print(f"Error: {e}")

def main():

    #Create output directory if it does not exist
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    #Creating Sample Sheet
    sample_sheet = create_gene_list(args.gwena_enrichment_file)

    #Seperating Module Genes
    module_gene_files = seperate_module_genes(sample_sheet, args.output_directory)

    #Running Metascape and GoFigure! for each module gene list
    for module_gene_file in module_gene_files:
        print(f"Running Metascape and GoFigure for {module_gene_file}")
        metascape_docker_run(module_gene_file, args.output_directory, args.metascape_download_location)
        GoFigure_run(module_gene_file, args.output_directory)

if __name__ == "__main__":
    main()