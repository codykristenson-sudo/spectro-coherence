#!/usr/bin/env python3
"""
WINERED Solar-Analog Coherence Analysis Example

Demonstrates spectro-coherence analysis on WINERED science-ready spectra.

Usage:
    python winered_analysis.py /path/to/winered/fits/files
    python winered_analysis.py /path/to/winered/fits/files --output report.pdf
"""

import sys
import argparse
from pathlib import Path
import numpy as np

from spectro_coherence import (
    load_winered_spectrum,
    load_multiple_spectra,
    calculate_c_index,
    c_index_statistics,
    coherence_quality_score,
    plot_spectrum_with_coherence,
    plot_coherence_distribution,
    plot_multiple_spectra_comparison,
    save_figure,
    get_snr_estimate
)


def analyze_single_spectrum(filepath, output_dir=None):
    """Analyze a single WINERED spectrum."""
    print(f"\nAnalyzing: {Path(filepath).name}")
    
    # Load spectrum
    spectrum = load_winered_spectrum(filepath)
    
    # Calculate C-Index
    positions, c_indices = calculate_c_index(spectrum.flux, window=200, step=100)
    
    # Get statistics
    stats = c_index_statistics(c_indices)
    snr = get_snr_estimate(spectrum)
    quality = coherence_quality_score(stats['mean'], stats['cv'])
    
    # Print results
    print(f"  Wavelength range: {spectrum.wave.min():.1f} - {spectrum.wave.max():.1f} Å")
    print(f"  Valid pixels: {len(spectrum.flux)}")
    print(f"  SNR (median): {snr:.1f}")
    print(f"  Mean C-Index: {stats['mean']:.4f} ± {stats['std']:.4f}")
    print(f"  C-Index range: [{stats['min']:.4f}, {stats['max']:.4f}]")
    print(f"  Coefficient of variation: {stats['cv']*100:.2f}%")
    print(f"  Quality assessment: {quality}")
    
    # Generate visualizations if output directory specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Spectrum with coherence overlay
        wave_pos = np.interp(positions, np.arange(len(spectrum.wave)), spectrum.wave)
        fig = plot_spectrum_with_coherence(spectrum, positions, c_indices, wave_pos)
        save_figure(fig, output_dir / f"{spectrum.target_name}_coherence.png")
        
        # Distribution
        fig = plot_coherence_distribution(c_indices, spectrum.target_name)
        save_figure(fig, output_dir / f"{spectrum.target_name}_distribution.png")
        
        print(f"  Saved plots to: {output_dir}")
    
    return {
        'spectrum': spectrum,
        'positions': positions,
        'c_indices': c_indices,
        'stats': stats,
        'snr': snr,
        'quality': quality
    }


def analyze_multiple_spectra(directory, pattern="*.fits", output_dir=None):
    """Analyze multiple WINERED spectra."""
    print(f"\nLoading spectra from: {directory}")
    print(f"Pattern: {pattern}")
    
    # Load all spectra
    spectra = load_multiple_spectra(
        directory, 
        pattern=pattern,
        loader_func=load_winered_spectrum
    )
    
    if not spectra:
        print("No spectra found!")
        return None
    
    print(f"Loaded {len(spectra)} spectra")
    
    # Analyze each
    results = {}
    for spectrum in spectra:
        positions, c_indices = calculate_c_index(spectrum.flux, window=200, step=100)
        stats = c_index_statistics(c_indices)
        snr = get_snr_estimate(spectrum)
        
        results[spectrum.target_name] = {
            'spectrum': spectrum,
            'positions': positions,
            'c_indices': c_indices,
            'stats': stats,
            'snr': snr,
            'quality': coherence_quality_score(stats['mean'], stats['cv'])
        }
    
    # Print summary
    print("\n" + "="*60)
    print("COHERENCE ANALYSIS SUMMARY")
    print("="*60)
    
    sorted_names = sorted(results.keys(), 
                         key=lambda x: results[x]['stats']['mean'], 
                         reverse=True)
    
    for i, name in enumerate(sorted_names, 1):
        r = results[name]
        print(f"{i}. {name:15s}  C = {r['stats']['mean']:.4f} ± {r['stats']['std']:.4f}  "
              f"SNR = {r['snr']:6.1f}  Quality: {r['quality']}")
    
    # Cross-target statistics
    all_means = [results[name]['stats']['mean'] for name in results.keys()]
    overall_mean = np.mean(all_means)
    overall_std = np.std(all_means)
    overall_cv = overall_std / overall_mean
    
    print(f"\nCross-Target Statistics:")
    print(f"  Overall C-Index: {overall_mean:.4f} ± {overall_std:.4f}")
    print(f"  Coefficient of Variation: {overall_cv:.3f}")
    
    if overall_cv < 0.05:
        print(f"  → High consistency across targets (excellent!)")
    elif overall_cv > 0.15:
        print(f"  → Significant variation across targets (investigate)")
    else:
        print(f"  → Moderate consistency across targets")
    
    # Generate comparison plot if output specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        fig = plot_multiple_spectra_comparison(results)
        save_figure(fig, output_dir / "coherence_comparison.png")
        print(f"\nSaved comparison plot to: {output_dir}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Analyze WINERED spectra using C-Index coherence framework"
    )
    parser.add_argument(
        'path',
        type=str,
        help='Path to FITS file or directory containing FITS files'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        default='*.fits',
        help='File pattern for directory mode (default: *.fits)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output directory for plots and reports'
    )
    
    args = parser.parse_args()
    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path not found: {path}")
        sys.exit(1)
    
    # Determine if single file or directory
    if path.is_file():
        analyze_single_spectrum(path, args.output)
    elif path.is_dir():
        analyze_multiple_spectra(path, args.pattern, args.output)
    else:
        print(f"Error: Invalid path: {path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
