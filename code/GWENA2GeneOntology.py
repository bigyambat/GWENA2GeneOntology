# GWENA2GeneOntology Package

# Conda Environment Setup
# conda create -n gwenav2
# conda activate gwenav2
# pip install pandas numpy docker openpyxl


# Command Line Usage:
# python GWENA2GeneOntology.py --gwena_enrichment_file /path/to/gwena_enrichment_file.xlsx --output_directory /path/to/output_directory --metascape_download_location /path/to/metascape_download_location

# Test Run
# /Users/bigyambat/miniforge3/envs/gwenav2/bin/python3 /Users/bigyambat/Desktop/GWENA2GeneOntology/code/GWENA2GeneOntology.py --gwena_enrichment_file /Users/bigyambat/Desktop/GWENA2GeneOntology/test_data/Enrichment_Complete.xlsx --output_directory /Users/bigyambat/Desktop/GWENA2GeneOntology/test_data/output_directory --metascape_download_location /Users/bigyambat/Desktop/GWENA2GeneOntology/msbio_v3.5.20240901

import pandas as pd
import numpy as np
import docker
import argparse
import subprocess
import os
import logging
from typing import List, Dict
from pathlib import Path

#Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class GWENAAnalysis:
    """Class to handle GWENA enrichment analysis operations"""
    def __init__(self, input_file: str, output_dir: str, metascape_location: str):
        self.input_file = input_file
        self.output_dir = Path(output_dir)
        self.metascape_location = Path(metascape_location)

        self._validate_inputs()

    def _validate_inputs(self) -> None:
        if not Path(self.input_file).exists():
            raise FileNotFoundError(f"Input file {self.input_file} not found")
        if not Path(self.metascape_location).exists():
            raise FileNotFoundError(f"Metascape location {self.metascape_location} not found")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_gene_list(self, sample_sheet: pd.DataFrame) -> List[Path]:
        """Create Gene List from GWENA Enrichment Data"""

        module_files = []
        module_path = Path(self.output_dir) / "module_gene_list"
        module_path.mkdir(exist_ok=True)

        try:
            for i in sample_sheet['query'].unique():
                try:
                    # Convert to int
                    i = int(i)
                except ValueError as e:
                    logger.error(f"Error converting {i} to int: {str(e)}")
                    continue

                module = sample_sheet[sample_sheet['query'] == i]
                file_path = module_path / f"module_{i}_gene_list.csv"
                module.to_csv(file_path, sep="\t", index=False)
                module_files.append(file_path)
       
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise 
        return module_files
    
    def select_GO_genes_and_pvalue(self, module_files: List[Path]) -> List[Path]:
        """Select genes from module files that are part of GO atlas"""
        
        go_module_path = Path(self.output_dir) / "go_gene_list"
        go_module_path.mkdir(exist_ok=True)
        
        filtered_module_files = []
        
        try:
            for module_file in module_files:
                try:
                    # Extract module number from filename
                    module_num = module_file.stem.split('_')[1]
                    
                    # Read the original module file
                    df = pd.read_csv(module_file, sep="\t")
                    
                    # Select only the genes and p-values
                    filtered_df = df[['gene', 'p_value']]
                    
                    # Here you would add logic to filter for genes in the GO atlas
                    # For example, if you have a list of GO genes:
                    # go_genes = set(pd.read_csv('path_to_go_genes.txt')['gene'])
                    # filtered_df = filtered_df[filtered_df['gene'].isin(go_genes)]
                    
                    # Create the output file path
                    go_file_path = go_module_path / f"module_{module_num}_go_genes.csv"
                    
                    # Save the filtered genes
                    filtered_df.to_csv(go_file_path, sep="\t", index=False)
                    filtered_module_files.append(go_file_path)
                    
                    logger.info(f"Created GO gene list for module {module_num}")
                    
                except Exception as e:
                    logger.error(f"Error selecting GO genes from {module_file}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in GO gene selection process: {str(e)}")
            raise
            
        return filtered_module_files

    def run_metascape_analysis(self, module_file: Path) -> None:
        """ Run Metascape container for gene analysis"""

        try:
            output_path = Path(self.output_dir) / "metascape" / module_file.stem
            output_path.mkdir(parents=True, exist_ok=True)

            command = [
                f"{self.metascape_location}/bin/ms.sh",
                "-u",
                "-o", str(output_path),
                str(module_file)
            ]

            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info(f"Completed Metascape analysis for {module_file.name}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Metascape Error: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Error running Metascape for {module_file.name}: {str(e)}")
            raise
    
    def run_go_figure_analysis(self, module_file: Path) -> None:
        """Run GoFigure analysis for gene ontology"""

        try:
            output_path = self.output_dir / "GoFigure" / module_file.stem
            output_path.mkdir(parents=True, exist_ok=True)

            command = [
                "python3",
                str(Path.home() /"miniforge3/pkgs/go-figure-1.0.2-hdfd78af_0/python-scripts/gofigure.py"),
                "-i", str(module_file),
                "-o", str(output_path),
            ]
            
            result = subprocess.run(command, capture_output=True, text=True)
            logger.info(f"Completed GoFigure analysis for {module_file.name}")
        
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running GoFigure for {module_file.name}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error running GoFigure for {module_file.name}: {str(e)}")
            raise

def main():
    # Create option parser
    parser = argparse.ArgumentParser(description='GWENA2GeneOntology')
    parser.add_argument('--gwena_enrichment_file', type=str, help='Input file path')
    parser.add_argument('--output_directory', type=str, help='Output directory path')
    parser.add_argument('--metascape_download_location', type=str, help='Metascape Docker image file location')
    args = parser.parse_args()

    try:
        logger.info("Starting GWENA2GeneOntology Analysis")
        # Loading in gwena enrichment file as sample sheet 
        sample_sheet = pd.read_excel(args.gwena_enrichment_file)    
    
        # Initialize Analysis
        analysis = GWENAAnalysis(args.gwena_enrichment_file, args.output_directory, args.metascape_download_location)

        # Create initial gene lists
        module_files = analysis.create_gene_list(sample_sheet)
        
        # Filter for GO genes
        go_module_files = analysis.select_GO_genes_and_pvalue(module_files)
        
        # Run analyses on the GO-filtered gene lists
        for module_file in go_module_files:
            logger.info(f"Running Metascape and GoFigure for {module_file}")
            analysis.run_metascape_analysis(module_file)
            analysis.run_go_figure_analysis(module_file)
        
        logger.info("Analysis Completed")
        
    except Exception as e:
        logger.error(f"Analysis Failed: {str(e)}")
        raise
        
if __name__ == "__main__":
    main()