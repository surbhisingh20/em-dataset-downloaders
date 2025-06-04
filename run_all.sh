#!/bin/bash

# EM Dataset Downloaders - Reproducibility Script
set -e

echo "Installing requirements..."
pip3 install -r requirements.txt

echo "Downloading datasets..."

# Download commands
python3 epfl_hippocampus/epfl_downloader.py --files 4 --threads 2
python3 flyem_hemibrain/hemibrain_downloader.py --size 100
python3 empiar_11759/empiar_downloader.py --files 3 --threads 2
python3 idr_0086/idr_downloader.py --files 2 --threads 2
python3 openorganelle_jrc/openorganelle_downloader.py --chunks 5

echo "Download complete. Check dataset directories for data and metadata files." 