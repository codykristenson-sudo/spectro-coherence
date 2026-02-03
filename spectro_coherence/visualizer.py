"""
Visualization Tools for Coherence Analysis

Generate publication-quality plots and charts for spectroscopic coherence analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from .cindex import c_index_statistics, detect_anomalies
from .fits_handler import SpectrumFITS


def plot_spectrum_with_coherence(
    spectrum: SpectrumFITS,
    positions: np.ndarray,
    c_indices: np.ndarray,
    wave_positions: Optional[np.ndarray] = None,
    figsize: Tuple[float, float] = (12, 4)
) -> Figure:
    """
    Plot spectrum with C-Index overlay.
    
    Parameters
    ----------
    spectrum : SpectrumFITS
        Spectrum object containing wavelength and flux
    positions : np.ndarray
        C-Index window positions (pixel coordinates)
    c_indices : np.ndarray
        Calculated C-Index values
    wave_positions : np.ndarray, optional
        C-Index positions in wavelength space (computed if not provided)
    figsize : tuple, default=(12, 4)
        Figure size (width, height) in inches
        
    Returns
    -------
    fig : Figure
        Matplotlib figure object
    """
    fig, ax1 = plt.subplots(1, 1, figsize=figsize)
    
    # Plot spectrum
    ax1.plot(spectrum.wave, spectrum.flux, 'b-', alpha=0.6, linewidth=0.5, label='Flux')
    ax1.set_ylabel('Normalized Flux', fontsize=10)
    ax1.set_xlabel('Wavelength (Å)', fontsize=10)
    ax1.set_title(f'{spectrum.target_name}', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0.7, 1.2)
    
    # Convert positions to wavelength if needed
    if wave_positions is None:
        wave_positions = np.interp(positions, np.arange(len(spectrum.wave)), spectrum.wave)
    
    # Overlay C-Index
    ax2 = ax1.twinx()
    ax2.plot(wave_positions, c_indices, 'r-', alpha=0.7, linewidth=1.5, label='C-Index')
    ax2.set_ylabel('C-Index', fontsize=10, color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.set_ylim(0.8, 1.0)
    
    # Mark anomalies
    stats = c_index_statistics(c_indices)
    anomaly_pos, anomaly_vals = detect_anomalies(positions, c_indices)
    if len(anomaly_pos) > 0:
        anomaly_wave = np.interp(anomaly_pos, np.arange(len(spectrum.wave)), spectrum.wave)
        ax2.scatter(anomaly_wave, anomaly_vals, color='red', s=50, 
                   marker='x', linewidths=2, zorder=5, label='Anomalies')
    
    plt.tight_layout()
    return fig


def plot_coherence_distribution(
    c_indices: np.ndarray,
    target_name: str = "",
    figsize: Tuple[float, float] = (6, 4)
) -> Figure:
    """
    Plot C-Index distribution histogram.
    
    Parameters
    ----------
    c_indices : np.ndarray
        Array of C-Index values
    target_name : str, optional
        Target name for plot title
    figsize : tuple, default=(6, 4)
        Figure size (width, height)
        
    Returns
    -------
    fig : Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    stats = c_index_statistics(c_indices)
    
    ax.hist(c_indices, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
    ax.axvline(stats['mean'], color='red', linestyle='--', linewidth=2, 
              label=f"Mean: {stats['mean']:.4f}")
    ax.axvline(stats['anomaly_threshold'], color='orange', linestyle='--', 
              linewidth=1, label=f"Threshold: {stats['anomaly_threshold']:.4f}")
    
    ax.set_xlabel('C-Index Value', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    title = 'C-Index Distribution'
    if target_name:
        title = f'{target_name}: {title}'
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_multiple_spectra_comparison(
    spectra_results: Dict[str, Dict],
    figsize: Tuple[float, float] = (14, 10)
) -> Figure:
    """
    Create comparative visualization for multiple spectra.
    
    Parameters
    ----------
    spectra_results : dict
        Dictionary mapping target names to results dictionaries containing:
        - 'c_indices': np.ndarray of C-Index values
        - 'stats': dict of statistics
    figsize : tuple, default=(14, 10)
        Figure size (width, height)
        
    Returns
    -------
    fig : Figure
        Matplotlib figure with comparative plots
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    names = sorted(spectra_results.keys())
    all_c_indices = {name: spectra_results[name]['c_indices'] for name in names}
    
    # 1. Box plot comparison
    ax = axes[0, 0]
    data_for_box = [all_c_indices[name] for name in names]
    bp = ax.boxplot(data_for_box, labels=names, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    ax.set_ylabel('C-Index', fontsize=11, fontweight='bold')
    ax.set_title('Cross-Target Coherence Comparison', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.tick_params(axis='x', rotation=45)
    
    # 2. Violin plot
    ax = axes[0, 1]
    positions = np.arange(1, len(names) + 1)
    for i, name in enumerate(names, 1):
        parts = ax.violinplot([all_c_indices[name]], positions=[i],
                             showmeans=True, showextrema=True)
        for pc in parts['bodies']:
            pc.set_facecolor('steelblue')
            pc.set_alpha(0.7)
    ax.set_xticks(positions)
    ax.set_xticklabels(names, rotation=45)
    ax.set_ylabel('C-Index', fontsize=11, fontweight='bold')
    ax.set_title('Coherence Distribution Comparison', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # 3. Mean coherence with error bars
    ax = axes[1, 0]
    means = [spectra_results[name]['stats']['mean'] for name in names]
    stds = [spectra_results[name]['stats']['std'] for name in names]
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(names)))
    
    bars = ax.bar(names, means, yerr=stds, capsize=5, alpha=0.7,
                  color=colors, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Mean C-Index', fontsize=11, fontweight='bold')
    ax.set_title('Mean Coherence with Uncertainty', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, mean, std in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 0.002,
               f'{mean:.4f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # 4. Consistency metric (CV)
    ax = axes[1, 1]
    cvs = [(spectra_results[name]['stats']['std'] / spectra_results[name]['stats']['mean']) * 100 
           for name in names]
    bars = ax.bar(names, cvs, alpha=0.7, color='coral', edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Coefficient of Variation (%)', fontsize=11, fontweight='bold')
    ax.set_title('Internal Coherence Consistency', fontsize=12, fontweight='bold')
    ax.axhline(y=2.0, color='red', linestyle='--', linewidth=2, label='Low variance threshold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    return fig


def save_figure(fig: Figure, filepath: Path, dpi: int = 300):
    """
    Save figure to file with appropriate settings.
    
    Parameters
    ----------
    fig : Figure
        Matplotlib figure to save
    filepath : Path or str
        Output filepath
    dpi : int, default=300
        Resolution in dots per inch
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
