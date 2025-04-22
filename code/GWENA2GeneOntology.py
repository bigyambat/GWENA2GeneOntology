# GWENA2GeneOntology Package

# Conda Environment Setup

# conda create -n gwenav2 python=3.10
# conda activate gwenav2
# conda install -c conda-forge matplotlib=3.7.1

# Obtain a free license for metascape at  https://metascape.org/msbio.html

# pip install pandas numpy docker openpyxl adjustText scikit-learn seaborn

# Command Line Usage:
# python GWENA2GeneOntology.py --gwena_enrichment_file /path/to/gwena_enrichment_file.xlsx --output_directory /path/to/output_directory --metascape_download_location /path/to/metascape_download_location --gene_list_excel /path/to/gene_list_file.xlsx

# Test Run
# /Users/bigyambat/miniforge3/envs/gwenav2/bin/python3 /Users/bigyambat/Desktop/GWENA2GeneOntology/code/GWENA2GeneOntology.py --gwena_enrichment_file /Users/bigyambat/Desktop/GWENA2GeneOntology/test_data/Enrichment_Complete.xlsx --output_directory /Users/bigyambat/Desktop/GWENA2GeneOntology/test_data/output_directory --metascape_download_location /Users/bigyambat/Desktop/GWENA2GeneOntology/msbio_v3.5.20240901 --gene_list_excel /Users/bigyambat/Desktop/GWENA2GeneOntology/test_data/Module_Genes_Post_Filtering.xlsx

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
    def __init__(self, input_file: str, output_dir: str, metascape_location: str, gene_list_excel: str = None):
        self.input_file = input_file
        self.output_dir = Path(output_dir)
        self.metascape_location = Path(metascape_location)
        self.gene_list_excel = gene_list_excel
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        logger.info("Validating inputs...")
        if not Path(self.input_file).exists():
            raise FileNotFoundError(f"Input file {self.input_file} not found")
        logger.info(f"Input file confirmed: {self.input_file}")

        if not Path(self.gene_list_excel).exists() and self.gene_list_excel:
            raise FileNotFoundError(f"Gene list Excel file {self.gene_list_excel} not found")
            logger.info("No gene list Excel file provided. Skipping Metascape Excel input.")

        if not Path(self.metascape_location).exists():
            raise FileNotFoundError(f"Metascape location {self.metascape_location} not found")
        logger.info(f"Metascape location confirmed: {self.metascape_location}")

        metascape_script = self.metascape_location / "bin" / "ms.sh"
        if not metascape_script.exists():
            raise FileNotFoundError(f"Metascape script not found at {metascape_script}")
        logger.info(f"Metascape script confirmed: {metascape_script}")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory created/confirmed: {self.output_dir}")

    def create_gene_list(self, sample_sheet: pd.DataFrame) -> List[Path]:
        logger.info("Creating module files using query values")

        if 'query' not in sample_sheet.columns:
            logger.error("Column 'query' not found in sample sheet")
            raise KeyError("Column 'query' not found in sample sheet")

        module_files = []
        module_path = self.output_dir / "module_gene_list"
        module_path.mkdir(exist_ok=True)

        for module_num in sample_sheet['query'].unique():
            try:
                module_num = int(module_num)
                module = sample_sheet[sample_sheet['query'] == module_num]
                ref_file_path = module_path / f"module_{module_num}_data.csv"
                module.to_csv(ref_file_path, sep="\t", index=False)
                logger.info(f"Saved module {module_num} data to {ref_file_path}")
                module_files.append(ref_file_path)
            except Exception as e:
                logger.error(f"Failed to process module {module_num}: {str(e)}")
                continue

        return module_files

    def select_GO_genes_and_pvalue(self, module_files: List[Path]) -> List[Path]:
        logger.info(f"Processing {len(module_files)} module files for GO analysis")
        return module_files

    def run_metascape_from_excel(self):
        if not self.gene_list_excel:
            logger.warning("No gene list Excel file provided. Skipping Metascape Excel input.")
            return

        logger.info(f"Running Metascape using gene list Excel file: {self.gene_list_excel}")

        license_path = self.metascape_location / "license" / "license.txt"

        if not license_path.exists():
            logger.error(f"License file not found at {license_path}")
            raise FileNotFoundError(f"License file not found at {license_path}")

        try:
            excel_data = pd.read_excel(self.gene_list_excel, sheet_name=None)
            for sheet_name, df in excel_data.items():
                if df.empty:
                    logger.warning(f"Sheet {sheet_name} is empty. Skipping.")
                    continue

                output_path = self.output_dir / "metascape_output" / f"module_{sheet_name}"
                output_path.mkdir(parents=True, exist_ok=True)

                gene_list_file = output_path / f"module_{sheet_name}_gene_list.txt"
                df.iloc[:, 0].dropna().to_csv(gene_list_file, index=False, header=False)

                metascape_script = self.metascape_location / "bin" / "ms.sh"

                command = ["docker", "run", "--rm",
                 "--platform", "linux/amd64",
                 "-v", str(license_path),  # mount license
                str(metascape_script), "-u", "-o", str(output_path), str(gene_list_file)]

                logger.info(f"Running Metascape command: {' '.join(command)}")

                result = subprocess.run(command, capture_output=True, text=True)
                logger.info("Metascape stdout:\n" + result.stdout)
                logger.info("Metascape stderr:\n" + result.stderr)

                if result.returncode != 0:
                    logger.error(f"Metascape Error for module {sheet_name}: {result.stderr}")
                else:
                    logger.info(f"Completed Metascape for module {sheet_name}. Output: {output_path}")

        except Exception as e:
            logger.error(f"Failed to run Metascape from Excel: {e}")
            raise

    def create_gofigure_input(self, module_df: pd.DataFrame, module_num: int, output_dir: Path) -> Path:
        logger.info(f"Creating GoFigure input for module {module_num}")
        if 'term_id' not in module_df.columns or 'p_value' not in module_df.columns:
            logger.error("Missing 'term_id' or 'p_value' column in module data")
            raise KeyError("Missing 'term_id' or 'p_value' column")

        filtered = module_df[module_df['term_id'].astype(str).str.startswith("GO:")]
        go_terms_with_pval = filtered[['term_id', 'p_value']]
        output_file = output_dir / f"module_{module_num}_gofigure.tsv"
        go_terms_with_pval.to_csv(output_file, sep="\t", index=False, header=False)
        logger.info(f"Saved GoFigure input file to {output_file}")
        return output_file

    def run_go_figure_analysis(self, module_file: Path) -> None:
        logger.info(f"Running GoFigure analysis for {module_file.name}")
        try:
            output_path = self.output_dir / "GoFigure" / module_file.stem
            output_path.mkdir(parents=True, exist_ok=True)

            module_df = pd.read_csv(module_file, sep="\t")
            module_num = int(module_df['query'].iloc[0]) if 'query' in module_df.columns else 0
            go_input_file = self.create_gofigure_input(module_df, module_num, output_path)

            gofigure_script = Path.home() / "miniforge3/pkgs/go-figure-1.0.2-hdfd78af_0/python-scripts/gofigure.py"
            if not gofigure_script.exists():
                conda_prefix = os.environ.get('CONDA_PREFIX')
                if conda_prefix:
                    gofigure_script = Path(conda_prefix) / "bin" / "gofigure.py"
            if not gofigure_script.exists():
                gofigure_script = "gofigure.py"
                logger.warning(f"GoFigure script not found at expected locations, trying command '{gofigure_script}'")
            else:
                logger.info(f"Found GoFigure script at {gofigure_script}")

            command = ["python3", str(gofigure_script), "-i", str(go_input_file), "-o", str(output_path)]
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode != 0:
                logger.error(f"GoFigure Error: {result.stderr}")
                logger.error(f"Command output: {result.stdout}")
                return

            logger.info(f"Completed GoFigure analysis for {module_file.name}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running GoFigure for {module_file.name}: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Error running GoFigure for {module_file.name}: {str(e)}")
            raise


def main():
    parser = argparse.ArgumentParser(description='GWENA2GeneOntology')
    parser.add_argument('--gwena_enrichment_file', type=str, help='Input file path')
    parser.add_argument('--output_directory', type=str, help='Output directory path')
    parser.add_argument('--metascape_download_location', type=str, help='Metascape Docker image file location')
    parser.add_argument('--gene_list_excel', type=str, help='Path to Excel file containing gene lists for Metascape (optional)')

    args = parser.parse_args()

    try:
        logger.info("Starting GWENA2GeneOntology Analysis")
        logger.info(f"Input file: {args.gwena_enrichment_file}")
        logger.info(f"Output directory: {args.output_directory}")
        logger.info(f"Metascape location: {args.metascape_download_location}")
        logger.info(f"Gene list Excel file: {args.gene_list_excel}")

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

        if sample_sheet.empty:
            logger.error("Sample sheet is empty! Please check your input file.")
            return

        logger.info("Sample of input data:")
        logger.info(f"\n{sample_sheet.head().to_string()}")

        analysis = GWENAAnalysis(args.gwena_enrichment_file, args.output_directory, args.metascape_download_location, args.gene_list_excel)
        module_files = analysis.create_gene_list(sample_sheet)

        if args.gene_list_excel:
            try:
                analysis.run_metascape_from_excel()
            except Exception as e:
                logger.error(f"Metascape analysis failed: {str(e)}")
                return

        if not module_files:
            logger.error("No module files were created! Analysis cannot continue.")
            return

        go_module_files = analysis.select_GO_genes_and_pvalue(module_files)
        if not go_module_files:
            logger.error("No files available for analysis!")
            return

        for module_file in go_module_files:
            try:
                analysis.run_go_figure_analysis(module_file)
            except Exception as e:
                logger.error(f"GoFigure analysis failed for {module_file}: {str(e)}")

        logger.info("Analysis Completed")

    except Exception as e:
        logger.error(f"Analysis Failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()