#!/usr/bin/env python3
"""
IDR-0086 Data Downloader
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
    """Download IDR-0086 3D FIB-SEM TIFF files."""
    parser = argparse.ArgumentParser(description="Download 3D FIB-SEM TIFF files from IDR-0086")
    parser.add_argument('--files', '-f', type=int, default=12, help='Number of TIFF volumes to download')
    parser.add_argument('--threads', '-t', type=int, default=4, help='Parallel download threads')
    
    args = parser.parse_args()
    
    # Setup
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    
    # Get all TIFF files from both directories
    ftp = ftplib.FTP("ftp.ebi.ac.uk")
    ftp.login()
    
    # Get files from processed directory
    ftp.cwd(f"{BASE_PATH}/20200610-ftp/experimentD/Miron_FIB-SEM/Miron_FIB-SEM_processed")
    processed_files = [f for f in ftp.nlst() if f.endswith(('.tif', '.tiff'))]
    
    # Get files from dropbox directory  
    ftp.cwd(f"{BASE_PATH}/20200714-dropbox")
    dropbox_files = [f for f in ftp.nlst() if f.endswith(('.tif', '.tiff'))]
    ftp.quit()
    
    # Create file list with full remote paths
    all_files = []
    for f in processed_files:
        all_files.append((f, f"20200610-ftp/experimentD/Miron_FIB-SEM/Miron_FIB-SEM_processed/{f}"))
    for f in dropbox_files:
        all_files.append((f, f"20200714-dropbox/{f}"))
    
    files_to_download = all_files[:args.files]
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = list(executor.map(download_file, files_to_download))
    
    # Create metadata
    metadata = {
        'dataset': 'IDR-0086 Human Chromatin Organization',
        'source': f'ftp://ftp.ebi.ac.uk{BASE_PATH}',
        'technique': 'Focused Ion Beam Scanning Electron Microscopy (FIB-SEM)',
        'sample': 'U2OS human osteosarcoma cells',
        'resolution_nm': [20, 20, 20],
        'format': 'Multi-page TIFF (200-500 slices per volume)',
        'total_available_files': len(all_files),
        'files_downloaded': len(results),
        'total_size_mb': sum(r['size_mb'] for r in results),
        'files': results,
        'created': datetime.now().isoformat()
    }
    
    with open(DOWNLOAD_DIR / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    main() 