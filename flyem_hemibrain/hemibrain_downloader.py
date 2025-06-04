#!/usr/bin/env python3
"""
FlyEM Hemibrain Dataset Downloader
"""

import json
import random
import argparse
import numpy as np
from pathlib import Path
from datetime import datetime
from cloudvolume import CloudVolume

class HemibrainDownloader:
    """Downloads random 1000x1000x1000 pixel crops from hemibrain EM data."""
    
    def __init__(self, output_dir: str = "hemibrain_data"):
        # Create data directory relative to this script
        script_dir = Path(__file__).parent
        self.output_dir = script_dir / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_url = 'precomputed://https://neuroglancer-janelia-flyem-hemibrain.storage.googleapis.com/emdata/clahe_yz/jpeg'
        
    def download(self, crop_size: int = 1000):
        """Download random EM crop from hemibrain."""
        em_vol = CloudVolume(self.data_url)
        shape = [em_vol.shape[2], em_vol.shape[1], em_vol.shape[0]]
        
        start = [random.randint(0, shape[i] - crop_size) for i in range(3)]
        end = [start[i] + crop_size for i in range(3)]
        
        data = em_vol[start[2]:end[2], start[1]:end[1], start[0]:end[0]]
        data = np.array(data)
        
        if data.ndim == 4:
            data = data[:,:,:,0]
        if data.shape != (crop_size, crop_size, crop_size):
            data = np.transpose(data, (2, 1, 0))
        
        crop_file = self.output_dir / f"hemibrain_crop_{crop_size}x{crop_size}x{crop_size}.npy"
        np.save(crop_file, data)
        
        metadata = {
            'dataset': 'FlyEM Hemibrain Drosophila Connectome',
            'source': self.data_url,
            'technique': 'Focused Ion Beam Scanning Electron Microscopy (FIB-SEM)',
            'sample': 'Adult Drosophila brain hemisphere',
            'resolution_nm': [8, 8, 8],
            'format': 'Random crops from 3D volume',
            'crop_size': crop_size,
            'coordinates': {'start': start, 'end': end},
            'files': [{
                'filename': f"hemibrain_crop_{crop_size}x{crop_size}x{crop_size}.npy",
                'shape': list(data.shape),
                'dtype': str(data.dtype),
                'size_mb': data.nbytes / (1024 * 1024),
                'stats': {
                    'min': int(data.min()),
                    'max': int(data.max()),
                    'mean': float(data.mean())
                }
            }],
            'created': datetime.now().isoformat()
        }
        
        with open(self.output_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return str(crop_file)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Download random hemibrain EM crop")
    parser.add_argument('--output', '-o', default='hemibrain_data', help='Output directory')
    parser.add_argument('--size', '-s', type=int, default=1000, help='Crop size (default: 1000)')
    
    args = parser.parse_args()
    
    downloader = HemibrainDownloader(args.output)
    downloader.download(args.size)

if __name__ == "__main__":
    main() 