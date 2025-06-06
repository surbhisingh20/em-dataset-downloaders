#!/usr/bin/env python3
"""
IDR-0086 Data Downloader
Downloads specific Figure S3B FIB-SEM files from IDR-0086
"""

import json
import argparse
import ftplib
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Create data directory relative to this script
SCRIPT_DIR = Path(__file__).parent
DOWNLOAD_DIR = SCRIPT_DIR / "idr_data"
BASE_PATH = "/pub/databases/IDR/idr0086-miron-micrographs"

def download_file(file_info):
    """Download a single TIFF file."""
    filename, remote_path = file_info
    local_path = DOWNLOAD_DIR / filename
    
    ftp = ftplib.FTP("ftp.ebi.ac.uk")
    ftp.login()
    
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f'RETR {BASE_PATH}/{remote_path}', f.write)
    ftp.quit()
    
    return {
        'filename': filename,
        'remote_path': remote_path,
        'size_bytes': local_path.stat().st_size,
        'size_mb': local_path.stat().st_size / (1024 * 1024)
    }

def main():
    """Download IDR-0086 Figure S3B FIB-SEM TIFF files."""
    parser = argparse.ArgumentParser(description="Download Figure S3B FIB-SEM files from IDR-0086")
    parser.add_argument('--threads', '-t', type=int, default=2, help='Parallel download threads')
    
    args = parser.parse_args()
    
    # Setup
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    
    # Target specific Figure S3B files
    target_files = [
        ("Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xy.tif", "20200610-ftp/experimentD/Miron_FIB-SEM/Miron_FIB-SEM_processed/Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xy.tif"),
        ("Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xz.tif", "20200610-ftp/experimentD/Miron_FIB-SEM/Miron_FIB-SEM_processed/Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xz.tif")
    ]
    
    # Download files in parallel
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = list(executor.map(download_file, target_files))
    
    # Create metadata
    metadata = {
        'dataset': 'IDR-0086 Human Chromatin Organization (Figure S3B)',
        'source': f'ftp://ftp.ebi.ac.uk{BASE_PATH}',
        'technique': 'Focused Ion Beam Scanning Electron Microscopy (FIB-SEM)',
        'sample': 'U2OS human osteosarcoma cells',
        'resolution_nm': [20, 20, 20],
        'format': 'Multi-page TIFF volumes (xy and xz projections)',
        'description': 'Figure S3B supplementary data showing FIB-SEM U2OS cell imaging',
        'files_downloaded': len(results),
        'total_size_mb': sum(r['size_mb'] for r in results),
        'files': results,
        'created': datetime.now().isoformat()
    }
    
    with open(DOWNLOAD_DIR / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    main() 