#!/usr/bin/env python3
"""
EPFL Hippocampus Data Downloader
"""

import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class EPFLDownloader:
    """Downloader for EPFL hippocampus dataset."""
    
    def __init__(self):
        # Create data directory relative to this script
        self.download_dir = Path(__file__).parent / "epfl_data"
        self.download_dir.mkdir(exist_ok=True)
        
        self.base_url = "https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/"
        
        self.files = [
            "training.tif",                 # Training data
            "training_groundtruth.tif",     # Training labels
            "testing.tif",                  # Testing data  
            "testing_groundtruth.tif",      # Testing labels
            "results_test.tif"              # Algorithm results
        ]
        
        self.urls = [f"{self.base_url}{filename}" for filename in self.files]
    
    def download_file(self, url_filename: tuple) -> dict:
        """Download a single TIFF file."""
        url, filename = url_filename
        local_path = self.download_dir / filename
        
        response = requests.get(url, stream=True)
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return {
            'filename': filename,
            'size_bytes': local_path.stat().st_size,
            'size_mb': local_path.stat().st_size / (1024 * 1024)
        }
    
    def download(self, num_files: int = 5, max_workers: int = 3) -> int:
        """Download specified number of TIFF files in parallel."""
        files_to_download = list(zip(self.urls[:num_files], self.files[:num_files]))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.download_file, files_to_download))
        
        # Create metadata
        metadata = {
            'dataset': 'EPFL Hippocampus Mitochondria Segmentation',
            'source_url': self.base_url,
            'technique': 'Transmission Electron Microscopy (TEM)',
            'sample': 'CA1 hippocampus region',
            'resolution_nm': [5, 5, 5],
            'files_downloaded': len(results),
            'total_size_mb': sum(r['size_mb'] for r in results),
            'files': results,
            'created': datetime.now().isoformat()
        }
        
        with open(self.download_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return len(results)

def main():
    """Download EPFL hippocampus TIFF files."""
    parser = argparse.ArgumentParser(description="Download EPFL hippocampus dataset")
    parser.add_argument('--files', '-f', type=int, default=5, help='Number of files to download')
    parser.add_argument('--threads', '-t', type=int, default=3, help='Parallel download threads')
    
    args = parser.parse_args()
    
    downloader = EPFLDownloader()
    downloader.download(args.files, args.threads)

if __name__ == "__main__":
    main() 