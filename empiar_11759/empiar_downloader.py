#!/usr/bin/env python3
"""
EMPIAR-11759 Data Downloader
"""

import json
import argparse
import ftplib
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class EMPIARDownloader:
    """FTP downloader for EMPIAR-11759 dataset."""
    
    def __init__(self):
        # Create data directory relative to this script
        self.download_dir = Path(__file__).parent / "empiar_data"
        self.download_dir.mkdir(exist_ok=True)
        self.ftp_host = "ftp.ebi.ac.uk"
        self.ftp_path = "/empiar/world_availability/11759/data"
    
    def get_dm3_files(self) -> list:
        """Get list of DM3 files from FTP server."""
        ftp = ftplib.FTP(self.ftp_host)
        ftp.login()
        ftp.cwd(self.ftp_path)
        
        files = []
        file_list = ftp.nlst()
        for filename in file_list:
            if filename.endswith('.dm3'):
                files.append(filename)
        
        ftp.quit()
        return sorted(files)
    
    def download_file(self, filename: str) -> dict:
        """Download a single DM3 file."""
        local_path = self.download_dir / filename
        
        ftp = ftplib.FTP(self.ftp_host)
        ftp.login()
        ftp.cwd(self.ftp_path)
        
        with open(local_path, 'wb') as f:
            ftp.retrbinary(f'RETR {filename}', f.write)
        
        ftp.quit()
        
        return {
            'filename': filename,
            'size_bytes': local_path.stat().st_size,
            'size_mb': local_path.stat().st_size / (1024 * 1024)
        }
    
    def download(self, num_files: int = 16, max_workers: int = 4) -> int:
        """Download specified number of DM3 files in parallel."""
        dm3_files = self.get_dm3_files()
        files_to_download = dm3_files[:num_files]
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.download_file, files_to_download))
        
        # Create metadata
        metadata = {
            'dataset': 'EMPIAR-11759 Zebrafish Retina Development',
            'source': f'ftp://{self.ftp_host}{self.ftp_path}',
            'technique': 'Serial Block-Face Scanning Electron Microscopy (SBF-SEM)',
            'sample': 'Zebrafish retina (55 hours post fertilization)',
            'resolution_nm': [8, 8, 50],
            'format': 'DM3 (Digital Micrograph)',
            'total_available_files': len(dm3_files),
            'files_downloaded': len(results),
            'total_size_mb': sum(r['size_mb'] for r in results),
            'files': results,
            'created': datetime.now().isoformat()
        }
        
        with open(self.download_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return len(results)

def main():
    """Download EMPIAR-11759 DM3 files."""
    parser = argparse.ArgumentParser(description="Download DM3 files from EMPIAR-11759")
    parser.add_argument('--files', '-f', type=int, default=16)
    parser.add_argument('--threads', '-t', type=int, default=4)
    
    args = parser.parse_args()
    
    downloader = EMPIARDownloader()
    downloader.download(args.files, args.threads)

if __name__ == "__main__":
    main() 