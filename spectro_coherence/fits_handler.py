"""
FITS File Handling for Spectroscopic Data

Generic FITS loading with specialized support for common spectroscopic formats.
"""

import numpy as np
from astropy.io import fits
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings


class SpectrumFITS:
    """
    Container for spectroscopic data loaded from FITS files.
    
    Attributes
    ----------
    filepath : Path
        Path to source FITS file
    wave : np.ndarray
        Wavelength array
    flux : np.ndarray
        Flux array (typically normalized)
    err : np.ndarray, optional
        Flux uncertainty array
    metadata : dict
        Header information and metadata
    """
    
    def __init__(
        self,
        filepath: Path,
        wave: np.ndarray,
        flux: np.ndarray,
        err: Optional[np.ndarray] = None,
        metadata: Optional[dict] = None
    ):
        self.filepath = filepath
        self.wave = wave
        self.flux = flux
        self.err = err
        self.metadata = metadata or {}
        
    @property
    def filename(self) -> str:
        """Return filename without path."""
        return self.filepath.name
        
    @property
    def target_name(self) -> str:
        """Extract target name from filename or metadata."""
        # Try metadata first
        if 'OBJECT' in self.metadata:
            return self.metadata['OBJECT']
        
        # Fall back to filename parsing
        name = self.filepath.stem
        # Remove common suffixes
        for suffix in ['_spectrum', '_spec', '_1d']:
            name = name.replace(suffix, '')
        return name
    
    def __repr__(self) -> str:
        return (f"SpectrumFITS('{self.filename}', "
                f"{len(self.wave)} pixels, "
                f"λ={self.wave.min():.1f}-{self.wave.max():.1f})")


def load_fits_spectrum(
    filepath: Path,
    wave_col: str = 'WAVE',
    flux_col: str = 'FLUX',
    err_col: Optional[str] = 'ERR',
    extension: int = 1
) -> SpectrumFITS:
    """
    Load spectrum from FITS binary table.
    
    Parameters
    ----------
    filepath : Path or str
        Path to FITS file
    wave_col : str, default='WAVE'
        Column name for wavelength array
    flux_col : str, default='FLUX'
        Column name for flux array
    err_col : str or None, default='ERR'
        Column name for uncertainty array (None to skip)
    extension : int, default=1
        FITS extension number containing table data
        
    Returns
    -------
    spectrum : SpectrumFITS
        Loaded spectrum object
        
    Raises
    ------
    FileNotFoundError
        If FITS file doesn't exist
    KeyError
        If required columns not found in FITS table
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"FITS file not found: {filepath}")
    
    with fits.open(filepath) as hdul:
        # Load data table
        try:
            data = hdul[extension].data
        except IndexError:
            raise ValueError(f"Extension {extension} not found in {filepath}")
        
        # Extract columns
        try:
            wave = data[wave_col]
            flux = data[flux_col]
        except KeyError as e:
            available = data.columns.names
            raise KeyError(
                f"Column {e} not found. Available columns: {available}"
            )
        
        # Load uncertainty if available
        err = None
        if err_col and err_col in data.columns.names:
            err = data[err_col]
        
        # Extract metadata from primary header
        metadata = {}
        for key, value in hdul[0].header.items():
            if key not in ['COMMENT', 'HISTORY', '']:
                metadata[key] = value
        
        # Add extension header info
        for key, value in hdul[extension].header.items():
            if key not in ['COMMENT', 'HISTORY', '', 'TTYPE1', 'TTYPE2', 'TTYPE3']:
                if key not in metadata:  # Don't overwrite primary header
                    metadata[key] = value
    
    return SpectrumFITS(filepath, wave, flux, err, metadata)


def load_winered_spectrum(filepath: Path) -> SpectrumFITS:
    """
    Load WINERED science-ready spectrum.
    
    WINERED-specific loader with appropriate column names and handling.
    
    Parameters
    ----------
    filepath : Path or str
        Path to WINERED FITS file
        
    Returns
    -------
    spectrum : SpectrumFITS
        Loaded WINERED spectrum with all available columns
        
    Notes
    -----
    WINERED FITS files typically contain:
    - WAVE: wavelength (Angstrom, air frame)
    - FLUX: telluric-corrected, normalized flux
    - ERR: flux uncertainty
    - TELLURIC: telluric transmission
    - FLUX_RAW: flux before telluric correction
    - MASK: quality mask (1=masked, 0=good)
    """
    filepath = Path(filepath)
    
    with fits.open(filepath) as hdul:
        data = hdul[1].data
        
        # Load core data
        wave = data['WAVE']
        flux = data['FLUX']
        err = data['ERR'] if 'ERR' in data.columns.names else None
        
        # Extract metadata
        metadata = {}
        for key, value in hdul[0].header.items():
            if key not in ['COMMENT', 'HISTORY', '']:
                metadata[key] = value
        
        # Store additional WINERED-specific columns in metadata
        if 'TELLURIC' in data.columns.names:
            metadata['telluric'] = data['TELLURIC']
        if 'FLUX_RAW' in data.columns.names:
            metadata['flux_raw'] = data['FLUX_RAW']
        if 'MASK' in data.columns.names:
            metadata['mask'] = data['MASK']
        if 'ORDER' in data.columns.names:
            metadata['order'] = data['ORDER']
    
    return SpectrumFITS(filepath, wave, flux, err, metadata)


def load_multiple_spectra(
    directory: Path,
    pattern: str = "*.fits",
    loader_func = load_fits_spectrum,
    **loader_kwargs
) -> List[SpectrumFITS]:
    """
    Load multiple FITS spectra from directory.
    
    Parameters
    ----------
    directory : Path or str
        Directory containing FITS files
    pattern : str, default="*.fits"
        Glob pattern for file matching
    loader_func : callable, default=load_fits_spectrum
        Function to use for loading individual files
    **loader_kwargs
        Additional arguments passed to loader function
        
    Returns
    -------
    spectra : list of SpectrumFITS
        List of loaded spectra, sorted by filename
        
    Examples
    --------
    >>> spectra = load_multiple_spectra('/data/spectra', pattern='*_spectrum.fits')
    >>> print(f"Loaded {len(spectra)} spectra")
    """
    directory = Path(directory)
    
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")
    
    files = sorted(directory.glob(pattern))
    
    if not files:
        warnings.warn(f"No files matching '{pattern}' found in {directory}")
        return []
    
    spectra = []
    for filepath in files:
        try:
            spectrum = loader_func(filepath, **loader_kwargs)
            spectra.append(spectrum)
        except Exception as e:
            warnings.warn(f"Failed to load {filepath.name}: {e}")
            continue
    
    return spectra


def get_snr_estimate(spectrum: SpectrumFITS) -> float:
    """
    Estimate median signal-to-noise ratio.
    
    Parameters
    ----------
    spectrum : SpectrumFITS
        Spectrum object with flux and error arrays
        
    Returns
    -------
    snr : float
        Median SNR estimate
        
    Notes
    -----
    Returns NaN if error array not available
    """
    if spectrum.err is None:
        return np.nan
    
    valid = (np.isfinite(spectrum.flux) & 
             np.isfinite(spectrum.err) & 
             (spectrum.err > 0))
    
    if not np.any(valid):
        return np.nan
    
    snr = spectrum.flux[valid] / spectrum.err[valid]
    return np.median(snr)
