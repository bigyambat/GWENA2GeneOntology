# GWENA2GeneOntology

**GWENA2GeneOntology** is a Python-based pipeline for integrating GWENA enrichment results with functional analysis tools—**Metascape** and **GoFigure!**. It streamlines module-wise GO term analysis, automating the generation of input files, Metascape enrichment, and GO term visualization.

---

## 🔧 Features

- Converts GWENA enrichment files into per-module datasets
- Automatically prepares input gene lists for Metascape
- Executes Metascape jobs via Docker using the MSBio toolkit
- Organizes and copies results for downstream usage
- Prepares and runs GoFigure! visualizations for GO terms

---

## 📦 Installation & Environment Setup

1. **Clone this Repository**

   ```bash
   git clone https://github.com/bigyambat/GWENA2GeneOntology.git
   cd GWENA2GeneOntology
   ```

2. **Set Up a Conda Environment**

   ```bash
   conda create -n gwenav2 python=3.10
   conda activate gwenav2
   ```

3. **Install Required Python Packages**

   ```bash
   pip install pandas numpy docker openpyxl adjustText scikit-learn seaborn
   conda install -c conda-forge matplotlib=3.7.1
   ```

4. **Ensure Docker Is Installed and Running**

   - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Verify it works by running:
     ```bash
     docker info
     ```

---

## 🧬 Metascape (MSBio) Setup

To perform enrichment analysis, you must download and configure the **Metascape for Bioinformaticians (MSBio)** toolkit.

1. **Go to the MSBio download page**:  
   🖎 **https://metascape.org/gp/index.html#/menu/msbio**

2. **Download the `msbio2` Docker package** after accepting the terms.

3. **Unpack the archive**:
   ```bash
   tar -xzvf msbio_v3.5.20250101.tar.gz
   ```

4. **Place your license** (requested from the same site) in the `license` subfolder:
   - `msbio_v3.5.20250101/license/license.txt`

5. The Metascape script for Docker will be located at:  
   `msbio_v3.5.20250101/bin/ms.sh`

### 🔹 MSBio Usage

- Minimum syntax for gene-list analysis (multi-gene list):

  ```bash
  bin/ms.sh -o /data/output_folder /data/input_list_file
  ```

- For **single-gene-list** format, add the `-u` flag:

  ```bash
  bin/ms.sh -u -o /data/output_folder /data/input_list_file
  ```

- On **Windows**, use:

  ```bash
  .\winbin\ms.bat -u -o /data/output_folder /data/input_list_file
  ```

- **Important:** both `output_folder` and `input_list_file` **must** be subdirectories of the `data/` folder inside the MSBio directory. They must start with `/data/` or `data/`, as the Docker container mounts that as its root working directory.

- If using **Singularity**, use `bin/sms.sh` instead of `bin/ms.sh`.

### ⚠️ MSBio Notes

- `-S` sets the source organism (default: human). Use `-S 10090` for mouse.
- `--option option.json`: Use a JSON config to customize analysis settings.
- Ensure Docker has at least 8GB of memory allocated to avoid crashes.

### 🔹 Batch Mode Using `.job` Files

- For running multiple tasks efficiently (e.g., multiple gene lists), use a job file with JSON-formatted lines:

  ```bash
  bin/ms.sh /data/job_file.job
  ```

- Each line should include:
  ```json
  {"input": "input_lists/module_X/gene_list.txt", "output": "outputs/module_X", "single": true, "taxon": 10090}
  ```

- Use `#` at the beginning of a line to comment it out.
- Results will be wrapped between `START>` and `COMPLETE>` markers in logs.

---

## 🚀 Command Line Usage

```bash
python GWENA2GeneOntology.py   --gwena_enrichment_file /path/to/enrichment_file.xlsx   --output_directory /path/to/output_dir   --metascape_download_location /path/to/msbio_directory   --gene_list_excel /path/to/module_gene_list.xlsx
```

### Argument Description

| Argument | Description |
|----------|-------------|
| `--gwena_enrichment_file` | Path to GWENA enrichment `.xlsx` or `.tsv` file |
| `--output_directory` | Directory to save results |
| `--metascape_download_location` | Path to unzipped MSBio folder |
| `--gene_list_excel` | (Optional) Excel file with gene lists by module (1 sheet per module) |

---

## ✅ Example Run

```bash
python GWENA2GeneOntology.py   --gwena_enrichment_file test_data/Enrichment_Complete.xlsx   --output_directory test_data/output_directory   --metascape_download_location msbio_v3.5.20250101   --gene_list_excel test_data/Module_Genes_Post_Filtering.xlsx
```

---

## 📁 Output Structure

- `module_gene_list/`: Cleaned per-module gene enrichment tables
- `metascape_results/`: MSBio GO enrichment results
- `GoFigure/`: Scatterplots of enriched GO terms per module

---

## ⚠️ Notes

- **MSBio license** is required. Visit [https://metascape.org/gp/index.html#/menu/msbio](https://metascape.org/gp/index.html#/menu/msbio) to request a free license.
- The default taxonomy ID used is for mouse (`10090`). Change it in the code if using human or another species.
- Make sure the `gofigure.py` script is available in your environment or PATH.

---

## 📚 Citations

If you use this pipeline, please cite the following tools:

- **Metascape (MSBio)**  
Zhou Y, Zhou B, Pache L, Chang M, Khodabakhshi AH, Tanaseichuk O, Benner C, Chanda SK. _Metascape provides a biologist-oriented resource for the analysis of systems-level datasets._ Nat Commun. 2019 Apr 3;10(1):1523. [https://doi.org/10.1038/s41467-019-09234-6](https://doi.org/10.1038/s41467-019-09234-6)

- **GoFigure!**  
Supek F, Mihelčić M. _GO-Figure! A tool for visualizing Gene Ontology term enrichment results._ Front Bioinform. 2021;1:638255. [https://www.frontiersin.org/articles/10.3389/fbinf.2021.638255/full](https://www.frontiersin.org/articles/10.3389/fbinf.2021.638255/full)

---

## 📬 Support

For issues or suggestions, open an issue at:  
[https://github.com/bigyambat/GWENA2GeneOntology/issues](https://github.com/bigyambat/GWENA2GeneOntology/issues)

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more details.
