#!/usr/bin/env python3
"""
OpenOrganelle JRC Dataset Downloader
"""

import json
import random
import requests
import argparse
from pathlib import Path
from datetime import datetime

class OpenOrganelleDownloader:
    
    def __init__(self):
        self.output_dir = Path(__file__).parent / "openorganelle_data"
        self.output_dir.mkdir(exist_ok=True)
        
        self.base_url = "https://openorganelle.janelia.org/datasets/jrc_mus-liver/zarr"
        
        # Available chunk ranges
        self.raw_em_dims = (9, 40, 41)  # z, y, x
        self.nuclei_dims = (2, 5, 6)   # z, y, x
    
    def download_chunk(self, chunk_type, z, y, x):
        """Download a single zarr chunk."""
        if chunk_type == "raw_em":
            url = f"{self.base_url}/jrc_mus-liver.zarr/em/fibsem-uint8/s0/{z}/{y}/{x}"
            filename = f"raw_em_{z}_{y}_{x}.zarr"
        else:  # nuclei
            url = f"{self.base_url}/jrc_mus-liver.zarr/labels/nuclei-cc/s2/{z}/{y}/{x}"
            filename = f"nuclei_{z}_{y}_{x}.zarr"
        
        local_path = self.output_dir / filename
        response = requests.get(url)
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        return {
            'filename': filename,
            'chunk_type': chunk_type,
            'coordinates': [z, y, x],
            'size_bytes': local_path.stat().st_size,
            'size_kb': local_path.stat().st_size / 1024
        }
    
    def get_random_chunks(self, num_chunks=4):
        """Generate random chunk coordinates."""
        chunks = []
        
        # Download mostly raw_em chunks (75%) with some nuclei (25%)
        raw_count = max(1, int(num_chunks * 0.75))
        nuclei_count = max(1, num_chunks - raw_count)
        
        # Random raw_em chunks
        for _ in range(raw_count):
            z = random.randint(0, self.raw_em_dims[0] - 1)
            y = random.randint(0, self.raw_em_dims[1] - 1)
            x = random.randint(0, self.raw_em_dims[2] - 1)
            chunks.append(("raw_em", z, y, x))
        
        # Random nuclei chunks
        for _ in range(nuclei_count):
            z = random.randint(0, self.nuclei_dims[0] - 1)
            y = random.randint(0, self.nuclei_dims[1] - 1)
            x = random.randint(0, self.nuclei_dims[2] - 1)
            chunks.append(("nuclei", z, y, x))
        
        return chunks
    
    def download(self, num_chunks=4):
        """Download random zarr chunks."""
        chunks_to_download = self.get_random_chunks(num_chunks)
        
        file_results = []
        total_size = 0
        
        for chunk_type, z, y, x in chunks_to_download:
            result = self.download_chunk(chunk_type, z, y, x)
            file_results.append(result)
            total_size += result['size_bytes']
        
        # Create metadata
        metadata = {
            'dataset': 'OpenOrganelle JRC Mouse Liver',
            'source': self.base_url,
            'technique': 'Enhanced Focused Ion Beam Scanning Electron Microscopy (FIB-SEM)',
            'sample': 'Mouse liver (C57BL/6J)',
            'resolution_nm': [4, 4, 4],
            'format': 'Zarr chunks (random sampling)',
            'files_downloaded': len(file_results),
            'total_size_mb': total_size / (1024 * 1024),
            'files': file_results,
            'created': datetime.now().isoformat()
        }
        
        with open(self.output_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return len(chunks_to_download)

def main():
    parser = argparse.ArgumentParser(description="Download random OpenOrganelle JRC chunks")
    parser.add_argument('--chunks', '-c', type=int, default=4, help='Number of chunks to download')
    
    args = parser.parse_args()
    
    downloader = OpenOrganelleDownloader()
    downloader.download(args.chunks)

if __name__ == "__main__":
    main() 