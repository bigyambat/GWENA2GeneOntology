# GWENA2GeneOntology Package

# Conda Environment Setup
# conda create -n gwenav2
# conda activate gwenav2
# pip install pandas numpy docker openpyxl matplotlib scikit-learn adjustText


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
import sys
from typing import List, Dict
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text


# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("gwena_analysis.log")
    ]
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
        logger.info(f"Validating inputs...")
        if not Path(self.input_file).exists():
            raise FileNotFoundError(f"Input file {self.input_file} not found")
        logger.info(f"Input file confirmed: {self.input_file}")
        
        if not Path(self.metascape_location).exists():
            raise FileNotFoundError(f"Metascape location {self.metascape_location} not found")
        logger.info(f"Metascape location confirmed: {self.metascape_location}")
        
        # Check if the metascape script exists
        metascape_script = self.metascape_location / "bin" / "ms.sh"
        if not metascape_script.exists():
            raise FileNotFoundError(f"Metascape script not found at {metascape_script}")
        logger.info(f"Metascape script confirmed: {metascape_script}")
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory created/confirmed: {self.output_dir}")
    
    def create_gene_list(self, sample_sheet: pd.DataFrame) -> List[Path]:
        """Create Gene List from GWENA Enrichment Data using query values"""
        logger.info(f"Creating module files using query values from sample sheet with {len(sample_sheet)} rows")
        
        # Data validation
        if sample_sheet.empty:
            logger.error("Sample sheet is empty!")
            raise ValueError("Sample sheet contains no data")
        
        # Check if 'query' column exists to identify modules
        if 'query' not in sample_sheet.columns:
            logger.error(f"Column 'query' not found in sample sheet. Available columns: {sample_sheet.columns.tolist()}")
            raise KeyError("Column 'query' not found in sample sheet")
        
        module_files = []
        module_path = Path(self.output_dir) / "module_gene_list"
        module_path.mkdir(exist_ok=True)
        logger.info(f"Created directory for module files: {module_path}")

        unique_queries = sample_sheet['query'].unique()
        logger.info(f"Found {len(unique_queries)} unique modules to process")

        try:
            for i in unique_queries:
                try:
                    # Convert to int for module number
                    module_num = int(i)
                    logger.info(f"Processing module {module_num}")
                except ValueError as e:
                    logger.error(f"Error converting {i} to int: {str(e)}")
                    continue

                # Filter data for this module
                module = sample_sheet[sample_sheet['query'] == i]
                logger.info(f"Module {module_num} has {len(module)} entries")
                
                # Create a list of query values
                query_values = [str(i)]  # Start with the module number itself
                
                # Save the list to a file - one query per line
                file_path = module_path / f"module_{module_num}_list.txt"
                with open(file_path, 'w') as f:
                    for value in query_values:
                        f.write(f"{value}\n")
                
                logger.info(f"Saved module {module_num} list to {file_path}")
                
                # Also save the original module data for reference
                ref_file_path = module_path / f"module_{module_num}_data.csv"
                module.to_csv(ref_file_path, sep="\t", index=False)
                logger.info(f"Saved module {module_num} data to {ref_file_path}")
                
                module_files.append(file_path)
        
        except Exception as e:
            logger.error(f"Error creating module lists: {str(e)}")
            raise 
            
        logger.info(f"Created {len(module_files)} module files")
        return module_files
    
    def select_GO_genes_and_pvalue(self, module_files: List[Path]) -> List[Path]:
        """Process module files to prepare for GO analysis"""
        logger.info(f"Processing {len(module_files)} module files for GO analysis")
        
        # Simply pass through the file paths
        logger.info(f"Using {len(module_files)} files for GO analysis")
        return module_files

    def run_metascape_analysis(self, module_file: Path) -> None:
        """ Run Metascape container for gene analysis"""
        logger.info(f"Running Metascape analysis for {module_file.name}")

        try:
            output_path = Path(self.output_dir) / "metascape" / module_file.stem
            output_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created Metascape output directory: {output_path}")

            # Verify input file has data
            if not module_file.exists():
                logger.error(f"Input file {module_file} does not exist. Skipping Metascape analysis.")
                return
                
            # Check file size
            if module_file.stat().st_size == 0:
                logger.error(f"Input file {module_file} is empty. Skipping Metascape analysis.")
                return
                
            logger.info(f"Using module file: {module_file}")
            
            # Build and verify the command
            metascape_script = self.metascape_location / "bin" / "ms.sh"
            if not metascape_script.exists():
                logger.error(f"Metascape script not found at {metascape_script}")
                return
                
            command = [
                str(metascape_script),
                "-u",  # Update mode
                "-o", str(output_path),  # Output directory
                str(module_file)  # Input file
            ]
            
            logger.info(f"Running Metascape command: {' '.join(command)}")
            
            # Run the command
            result = subprocess.run(command, capture_output=True, text=True)
            
            # Check for errors
            if result.returncode != 0:
                logger.error(f"Metascape Error: {result.stderr}")
                logger.error(f"Command output: {result.stdout}")
                return
                
            logger.info(f"Completed Metascape analysis for {module_file.name}")
            logger.info(f"Output saved to {output_path}")
            
            # Verify output was created
            output_files = list(output_path.glob('*'))
            logger.info(f"Generated {len(output_files)} output files")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Metascape Error: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Error running Metascape for {module_file.name}: {str(e)}")
            raise
    
    def run_go_figure_analysis(self, module_file: Path) -> None:
        """Run GoFigure analysis for gene ontology"""
        logger.info(f"Running GoFigure analysis for {module_file.name}")

        try:
            output_path = self.output_dir / "GoFigure" / module_file.stem
            output_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created GoFigure output directory: {output_path}")

            # Find GoFigure script location
            # This is based on the path in the original code, you may need to adjust
            gofigure_script = Path.home() / "miniforge3/pkgs/go-figure-1.0.2-hdfd78af_0/python-scripts/gofigure.py"
            
            # Alternative locations to check if the above doesn't exist
            if not gofigure_script.exists():
                # Try to find it in the current environment
                conda_prefix = os.environ.get('CONDA_PREFIX')
                if conda_prefix:
                    gofigure_script = Path(conda_prefix) / "bin" / "gofigure.py"
                
            # If we still can't find it, try using just the command name
            if not gofigure_script.exists():
                gofigure_script = "gofigure.py"
                logger.warning(f"GoFigure script not found at expected locations, trying command '{gofigure_script}'")
            else:
                logger.info(f"Found GoFigure script at {gofigure_script}")

            # Read the module file
            if not module_file.exists():
                logger.error(f"Input file {module_file} does not exist. Skipping GoFigure analysis.")
                return
                
            # Check if this is a text file with module data
            try:
                with open(module_file, 'r') as f:
                    lines = [line.strip() for line in f if line.strip()]
                
                values = lines[1:] if len(lines) > 1 else [] #Skiping header line since GOFigure! does not expect a header

                logger.info(f"Loaded {len(values)} values from {module_file}")
                
                # Create a temporary file with the values for GoFigure
                temp_file = output_path / "values_for_gofigure.txt"
                with open(temp_file, 'w') as f:
                    for value in values:
                        f.write(f"{value}\n")
                
                logger.info(f"Created temporary file for GoFigure: {temp_file}")
                
                command = [
                    "python3",
                    str(gofigure_script),
                    "-i", str(temp_file),
                    "-o", str(output_path),
                ]
                
                logger.info(f"Running GoFigure command: {' '.join(command)}")
                
                result = subprocess.run(command, capture_output=True, text=True)
                
                # Check for errors
                if result.returncode != 0:
                    logger.error(f"GoFigure Error: {result.stderr}")
                    logger.error(f"Command output: {result.stdout}")
                    return
                    
                logger.info(f"Completed GoFigure analysis for {module_file.name}")
                logger.info(f"Output saved to {output_path}")
                
                # Verify output was created
                output_files = list(output_path.glob('*'))
                logger.info(f"Generated {len(output_files)} output files")
                
            except Exception as e:
                logger.error(f"Error processing file for GoFigure: {str(e)}")
                return
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running GoFigure for {module_file.name}: {e.stderr}")
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
        logger.info(f"Input file: {args.gwena_enrichment_file}")
        logger.info(f"Output directory: {args.output_directory}")
        logger.info(f"Metascape location: {args.metascape_download_location}")
        
        # Loading in gwena enrichment file as sample sheet
        logger.info("Loading GWENA enrichment file...")
        
        # Try to load as Excel first
        try:
            sample_sheet = pd.read_excel(args.gwena_enrichment_file)
            logger.info("Successfully loaded Excel file")
        except Exception as e:
            logger.warning(f"Failed to load as Excel: {str(e)}. Trying CSV...")
            try:
                sample_sheet = pd.read_csv(args.gwena_enrichment_file, sep="\t")
                logger.info("Successfully loaded CSV file")
            except Exception as e2:
                logger.error(f"Failed to load as CSV: {str(e2)}")
                raise ValueError("Could not load input file as Excel or CSV")
        
        logger.info(f"Loaded sample sheet with {len(sample_sheet)} rows and columns: {sample_sheet.columns.tolist()}")
        
        # If sample sheet is empty, exit
        if sample_sheet.empty:
            logger.error("Sample sheet is empty! Please check your input file.")
            return
            
        # Save a sample of the data for debugging
        logger.info("Sample of input data:")
        logger.info(f"\n{sample_sheet.head().to_string()}")
    
        # Initialize Analysis
        analysis = GWENAAnalysis(args.gwena_enrichment_file, args.output_directory, args.metascape_download_location)

        # Create module files using query values
        logger.info("Creating module files using query values...")
        module_files = analysis.create_gene_list(sample_sheet)
        logger.info(f"Created {len(module_files)} module files")
        
        # If no module files were created, exit
        if not module_files:
            logger.error("No module files were created! Analysis cannot continue.")
            return
        
        # Process for GO analysis
        logger.info("Processing for GO analysis...")
        go_module_files = analysis.select_GO_genes_and_pvalue(module_files)
        logger.info(f"Using {len(go_module_files)} files for analysis")
        
        # If no files are available for analysis, exit
        if not go_module_files:
            logger.error("No files available for analysis!")
            return
        
        # Run analyses
        for module_file in go_module_files:
            logger.info(f"Running analyses for {module_file}")
            try:
                analysis.run_metascape_analysis(module_file)
            except Exception as e:
                logger.error(f"Metascape analysis failed for {module_file}: {str(e)}")
                
            try:
                analysis.run_go_figure_analysis(module_file)
            except Exception as e:
                logger.error(f"GoFigure analysis failed for {module_file}: {str(e)}")
        
        logger.info("Analysis Completed")
        
    except Exception as e:
        logger.error(f"Analysis Failed: {str(e)}")
        raise
        
if __name__ == "__main__":
    main()