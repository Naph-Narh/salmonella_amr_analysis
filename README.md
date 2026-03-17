# Salmonella AMR Analysis

This repository contains a genomic analysis of antimicrobial resistance (AMR) genes in Salmonella isolates using **AMRFinderPlus**.

## Dataset

- Source: NCBI genomes
- Number of genomes: 100
- Assembly level: contigs
- Metadata includes: isolation source, geographic location, year of isolation

## Workflow

1. Download Salmonella genomes from NCBI
2. Run AMRFinderPlus to detect AMR genes
3. Process AMRFinderPlus results using Python scripts
4. Generate summary tables and figures
5. Compile results into a report

## Folder Structure

- `data/`: genome metadata
- `scripts/`: analysis scripts
- `results/`: raw and processed AMRFinderPlus output
- `figures/`: plots 
- `report/`: final report

## Usage

```bash
# Run AMRFinderPlus on all genomes
python3 scripts/run_amrfinder.py

# Process results and generate figures
python3 scripts/data_processing.py

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
