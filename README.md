# EM Dataset Downloaders

Collection of downloaders for 5 electron microscopy datasets, organized in a hierarchical structure with standardized metadata extraction and consolidation tools.

## Available Datasets

### 1. EPFL Hippocampus Mitochondria Segmentation
- **Location**: `epfl_hippocampus/`
- **Resolution**: 5×5×5 nm (isotropic)
- **Technique**: Transmission Electron Microscopy (TEM)
- **Sample**: CA1 hippocampus region
- **Files**: 1 file (123.9 MB)

### 2. FlyEM Hemibrain Drosophila Connectome
- **Location**: `flyem_hemibrain/`
- **Resolution**: 8×8×8 nm (isotropic)
- **Technique**: Focused Ion Beam Scanning Electron Microscopy (FIB-SEM)
- **Sample**: Adult Drosophila brain hemisphere
- **Files**: Random 1000³ pixel crops

### 3. EMPIAR-11759 Zebrafish Retina Development
- **Location**: `empiar_11759/`
- **Resolution**: 8×8×50 nm (anisotropic, 6.25× Z-axis)
- **Technique**: Serial Block-Face Scanning Electron Microscopy (SBF-SEM)
- **Sample**: Zebrafish retina (55 hours post fertilization)
- **Files**: 2 files (58.0 MB)

### 4. IDR-0086 Human Chromatin Organization
- **Location**: `idr_0086/`
- **Resolution**: 20×20×20 nm (isotropic)
- **Technique**: Focused Ion Beam Scanning Electron Microscopy (FIB-SEM)
- **Sample**: U2OS human osteosarcoma cells
- **Files**: 2 files (708.4 MB)

### 5. OpenOrganelle JRC Mouse Liver
- **Location**: `openorganelle_jrc/`
- **Resolution**: 4×4×4 nm (isotropic, highest resolution)
- **Technique**: Enhanced Focused Ion Beam Scanning Electron Microscopy (FIB-SEM)
- **Sample**: Mouse liver (C57BL/6J)
- **Files**: 4 zarr chunks (0.003 MB)


## Usage

### Download All Datasets
```bash
./run_all.sh
```

### Download Individual Datasets
```bash
cd epfl_hippocampus && python3 epfl_downloader.py
cd flyem_hemibrain && python3 hemibrain_downloader.py
cd empiar_11759 && python3 empiar_downloader.py
cd idr_0086 && python3 idr_downloader.py
cd openorganelle_jrc && python3 openorganelle_downloader.py
```

### Metadata Consolidation
```bash
python3 metadata_consolidator.py
```

This generates:
- `metadata_consolidated_report.json`: Complete structured analysis
- Console output with comparison table and key findings

## Metadata Analysis

The metadata consolidator extracts and compares:

### Common Fields (5/5 datasets)
- **Resolution**: Voxel size in nanometers [x,y,z]
- **Imaging Technique**: Type of electron microscopy
- **Sample Type**: Biological specimen description
- **File Count**: Number of downloaded files
- **Creation Time**: ISO timestamp

### Resolution Range
- **Highest**: 4×4×4 nm (OpenOrganelle JRC)
- **Lowest**: 20×20×20 nm (IDR-0086)
- **Anisotropic**: 8×8×50 nm (EMPIAR-11759, 6.25× Z-axis)
- **Isotropic**: 4/5 datasets

### Technique Distribution
- **FIB-SEM**: 3 datasets (60%)
- **SBF-SEM**: 1 dataset (20%)
- **TEM**: 1 dataset (20%)

### Organism Diversity
5 different organisms across phylogeny:
- Drosophila melanogaster (invertebrate)
- Danio rerio (fish)
- Mus musculus (mouse)
- Homo sapiens (human)
- Mammalian (unspecified)

## Dependencies

Install with: `pip install -r requirements.txt`

Core packages:
- requests (HTTP downloads)
- numpy (array operations)
- cloud-volume (neuroglancer data)
- zarr (chunked arrays)

## Files Generated

Each dataset creates:
- Downloaded data files in respective `*_data/` directories
- `metadata.json` with standardized technical specifications
- Console output confirming successful downloads

## Technical Specifications Summary

| Dataset | Resolution | Isotropic | Files | Size (MB) | Technique |
|---------|------------|-----------|-------|-----------|-----------|
| OpenOrganelle | 4×4×4 nm | ✓ | 4 | 0.003 | Enhanced FIB-SEM |
| EPFL Hippocampus | 5×5×5 nm | ✓ | 1 | 123.9 | TEM |
| FlyEM Hemibrain | 8×8×8 nm | ✓ | 1 | 1.0 | FIB-SEM |
| EMPIAR-11759 | 8×8×50 nm | ✗ | 2 | 58.0 | SBF-SEM |
| IDR-0086 | 20×20×20 nm | ✓ | 2 | 708.4 | FIB-SEM |

This collection provides diverse EM datasets spanning 4 orders of magnitude in file size (KB to GB) and multiple imaging techniques across 5 different organisms. 