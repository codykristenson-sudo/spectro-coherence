"""
spectro-coherence: Coherence Analysis for Astronomical Spectroscopy

A Python package implementing the C-Index (Coherence Index) framework
for quality assessment of spectroscopic data.

Main Components
---------------
cindex : Core C-Index calculation functions
fits_handler : FITS file loading and handling
visualizer : Plotting and visualization tools
reporter : Report generation utilities

Quick Start
-----------
>>> from spectro_coherence import load_fits_spectrum, calculate_c_index
>>> spectrum = load_fits_spectrum('spectrum.fits')
>>> positions, c_values = calculate_c_index(spectrum.flux)
>>> print(f"Mean coherence: {c_values.mean():.4f}")

References
----------
Kristenson, C.A. (2024-2026). Emergent Order Systems (EOS) Framework Series.
Zenodo. https://zenodo.org/communities/eos-framework
"""

__version__ = "1.0.0"
__author__ = "Cody A. Kristenson"
__license__ = "MIT"

# Core functionality
from .cindex import (
    calculate_c_index,
    c_index_statistics,
    detect_anomalies,
    coherence_quality_score
)

# FITS handling
from .fits_handler import (
    SpectrumFITS,
    load_fits_spectrum,
    load_winered_spectrum,
    load_multiple_spectra,
    get_snr_estimate
)

# Visualization
from .visualizer import (
    plot_spectrum_with_coherence,
    plot_coherence_distribution,
    plot_multiple_spectra_comparison,
    save_figure
)

__all__ = [
    # Version info
    '__version__',
    '__author__',
    
    # Core C-Index functions
    'calculate_c_index',
    'c_index_statistics',
    'detect_anomalies',
    'coherence_quality_score',
    
    # FITS handling
    'SpectrumFITS',
    'load_fits_spectrum',
    'load_winered_spectrum',
    'load_multiple_spectra',
    'get_snr_estimate',
    
    # Visualization
    'plot_spectrum_with_coherence',
    'plot_coherence_distribution',
    'plot_multiple_spectra_comparison',
    'save_figure',
]
