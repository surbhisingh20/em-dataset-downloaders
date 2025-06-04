#!/usr/bin/env python3
"""
Simple EM Dataset Metadata Consolidator
"""

import json
from pathlib import Path
from collections import defaultdict

def load_metadata():
    """Load all metadata files."""
    paths = {
        'EPFL': 'epfl_hippocampus/epfl_data/metadata.json',
        'FlyEM': 'flyem_hemibrain/hemibrain_data/metadata.json', 
        'EMPIAR': 'empiar_11759/empiar_data/metadata.json',
        'IDR': 'idr_0086/idr_data/metadata.json',
        'OpenOrganelle': 'openorganelle_jrc/openorganelle_data/metadata.json'
    }
    
    datasets = {}
    for name, path in paths.items():
        if Path(path).exists():
            with open(path) as f:
                datasets[name] = json.load(f)
    return datasets

def extract_common_fields(datasets):
    """Extract and analyze key fields."""
    extracted = {}
    analysis = {}
    
    for name, data in datasets.items():
        # Extract basic fields
        extracted[name] = {
            'resolution_nm': data.get('resolution_nm', []),
            'technique': data.get('technique', ''),
            'sample': data.get('sample', ''),
            'files_count': data.get('files_downloaded', 0),
            'size_mb': data.get('total_size_mb', 0)
        }
        
        # Analyze resolution
        res = data.get('resolution_nm', [])
        if res and len(res) == 3:
            analysis[name] = {
                'resolution': res,
                'isotropic': res[0] == res[1] == res[2],
                'min_nm': min(res),
                'max_nm': max(res)
            }
    
    return extracted, analysis

def group_techniques(datasets):
    """Group datasets by imaging technique."""
    groups = defaultdict(list)
    for name, data in datasets.items():
        tech = data.get('technique', '').split('(')[0].strip()
        groups[tech].append(name)
    return dict(groups)

def generate_table(extracted, analysis):
    """Generate comparison table."""
    datasets = list(extracted.keys())
    
    table = "\n" + "="*80 + "\n"
    table += "EM DATASET COMPARISON\n"
    table += "="*80 + "\n"
    table += f"{'Field':<20} | " + " | ".join(f"{d:<12}" for d in datasets) + "\n"
    table += "-" * 80 + "\n"
    
    # Resolution
    table += f"{'Resolution (nm)':<20} | "
    for dataset in datasets:
        res = analysis.get(dataset, {}).get('resolution', [])
        res_str = f"{res[0]}×{res[1]}×{res[2]}" if len(res) == 3 else "N/A"
        table += f"{res_str:<12} | "
    table += "\n"
    
    # Isotropic
    table += f"{'Isotropic':<20} | "
    for dataset in datasets:
        iso = "✓" if analysis.get(dataset, {}).get('isotropic', False) else "✗"
        table += f"{iso:<12} | "
    table += "\n"
    
    # Files and Size
    for field, key in [('Files', 'files_count'), ('Size (MB)', 'size_mb')]:
        table += f"{field:<20} | "
        for dataset in datasets:
            val = extracted[dataset][key] or 0
            if key == 'size_mb':
                table += f"{val:<12.1f} | "
            else:
                table += f"{val:<12} | "
        table += "\n"
    
    table += "="*80 + "\n"
    return table

def main():
    """Main consolidation function."""
    print("EM Dataset Metadata Consolidator")
    print("=" * 40)
    
    # Load and process data
    datasets = load_metadata()
    print(f"Loaded {len(datasets)} datasets")
    
    extracted, analysis = extract_common_fields(datasets)
    techniques = group_techniques(datasets)
    
    # Generate and save report
    report = {
        'summary': {'total_datasets': len(datasets), 'datasets': list(datasets.keys())},
        'fields': extracted,
        'resolution_analysis': analysis,
        'technique_groups': techniques,
        'table': generate_table(extracted, analysis)
    }
    
    with open('metadata_consolidated_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print results
    print(report['table'])
    print("KEY FINDINGS:")
    if analysis:
        min_res = min(a['min_nm'] for a in analysis.values())
        max_res = max(a['max_nm'] for a in analysis.values())
        iso_count = sum(1 for a in analysis.values() if a['isotropic'])
        print(f"- Resolution range: {min_res}-{max_res} nm")
        print(f"- Isotropic datasets: {iso_count}/{len(analysis)}")
    
    print(f"- Technique groups: {len(techniques)}")
    for tech, datasets_list in techniques.items():
        print(f"  • {tech}: {len(datasets_list)} datasets")

if __name__ == "__main__":
    main() 