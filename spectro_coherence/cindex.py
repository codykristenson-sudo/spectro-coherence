"""
C-Index (Coherence Index) Core Calculations

Implementation of the Kristenson C-Index framework for spectroscopic coherence analysis.
Published framework - stable, validated methodology.

References:
    Kristenson, C.A. (2024-2026). Emergent Order Systems (EOS) Framework Series. 
    Zenodo. https://zenodo.org/communities/eos-framework
"""

import numpy as np
from typing import Tuple, Optional


def calculate_c_index(
    data: np.ndarray,
    window: int = 100,
    step: int = 50,
    min_valid_fraction: float = 0.8
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate C-Index over sliding windows.
    
    C-Index measures spectral coherence through three normalized components:
    1. Smoothness: Inverse of normalized gradient magnitude
    2. Stability: Inverse coefficient of variation
    3. Consistency: Normalized autocorrelation (lag-1)
    
    Combined C-Index = (Smoothness + Stability + Consistency) / 3
    Range: [0, 1] where 1 represents perfect coherence
    
    Parameters
    ----------
    data : np.ndarray
        1D array of spectral flux values
    window : int, default=100
        Window size in pixels for sliding analysis
    step : int, default=50
        Step size for window advancement
    min_valid_fraction : float, default=0.8
        Minimum fraction of valid (non-NaN) data points required per window
        
    Returns
    -------
    positions : np.ndarray
        Center positions of each analysis window (in pixel coordinates)
    c_indices : np.ndarray
        Calculated C-Index values for each window
        
    Notes
    -----
    - Windows with insufficient valid data are skipped
    - NaN values are filtered before calculation
    - All three components equally weighted in final C-Index
    
    Examples
    --------
    >>> flux = np.random.normal(1.0, 0.05, 1000)  # Simulated spectrum
    >>> positions, c_values = calculate_c_index(flux, window=200, step=100)
    >>> mean_coherence = np.mean(c_values)
    """
    n = len(data)
    c_indices = []
    positions = []
    
    for i in range(0, n - window, step):
        segment = data[i:i+window]
        
        # Skip if insufficient valid data
        if np.sum(np.isfinite(segment)) < window * min_valid_fraction:
            continue
            
        # Remove NaNs for calculation
        segment = segment[np.isfinite(segment)]
        
        if len(segment) < 10:
            continue
        
        # 1. Smoothness: inverse of normalized gradient
        gradient = np.abs(np.diff(segment))
        smoothness = 1.0 / (1.0 + np.mean(gradient) / (np.std(segment) + 1e-10))
        
        # 2. Stability: inverse coefficient of variation
        mean_val = np.mean(segment)
        if abs(mean_val) > 1e-10:
            cv = np.std(segment) / abs(mean_val)
            stability = 1.0 / (1.0 + cv)
        else:
            stability = 0.5
        
        # 3. Consistency: temporal autocorrelation
        if len(segment) > 1:
            autocorr = np.corrcoef(segment[:-1], segment[1:])[0, 1]
            consistency = (autocorr + 1) / 2 if np.isfinite(autocorr) else 0.5
        else:
            consistency = 0.5
        
        # Combined C-Index (equal weighting)
        c_index = (smoothness + stability + consistency) / 3.0
        
        c_indices.append(c_index)
        positions.append(i + window / 2)
    
    return np.array(positions), np.array(c_indices)


def c_index_statistics(c_indices: np.ndarray) -> dict:
    """
    Calculate summary statistics for C-Index values.
    
    Parameters
    ----------
    c_indices : np.ndarray
        Array of C-Index values
        
    Returns
    -------
    stats : dict
        Dictionary containing:
        - mean: Mean C-Index
        - std: Standard deviation
        - min: Minimum value
        - max: Maximum value
        - cv: Coefficient of variation (std/mean)
        - anomaly_threshold: Mean - 2*std (2-sigma threshold)
        - n_values: Number of values
    """
    return {
        'mean': np.mean(c_indices),
        'std': np.std(c_indices),
        'min': np.min(c_indices),
        'max': np.max(c_indices),
        'cv': np.std(c_indices) / np.mean(c_indices) if np.mean(c_indices) > 0 else 0,
        'anomaly_threshold': np.mean(c_indices) - 2 * np.std(c_indices),
        'n_values': len(c_indices)
    }


def detect_anomalies(
    positions: np.ndarray,
    c_indices: np.ndarray,
    threshold_sigma: float = 2.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Detect coherence anomalies using statistical threshold.
    
    Parameters
    ----------
    positions : np.ndarray
        Window center positions
    c_indices : np.ndarray
        Calculated C-Index values
    threshold_sigma : float, default=2.0
        Number of standard deviations below mean to define anomaly
        
    Returns
    -------
    anomaly_positions : np.ndarray
        Positions of detected anomalies
    anomaly_values : np.ndarray
        C-Index values at anomaly positions
    """
    threshold = np.mean(c_indices) - threshold_sigma * np.std(c_indices)
    anomaly_mask = c_indices < threshold
    
    return positions[anomaly_mask], c_indices[anomaly_mask]


def coherence_quality_score(mean_c: float, cv: float) -> str:
    """
    Assign qualitative quality score based on coherence metrics.
    
    Parameters
    ----------
    mean_c : float
        Mean C-Index value
    cv : float
        Coefficient of variation
        
    Returns
    -------
    quality : str
        Quality assessment: 'Excellent', 'Good', 'Fair', or 'Poor'
        
    Notes
    -----
    Scoring criteria:
    - Excellent: mean > 0.85 and cv < 0.05
    - Good: mean > 0.80 and cv < 0.10
    - Fair: mean > 0.70 and cv < 0.15
    - Poor: otherwise
    """
    if mean_c > 0.85 and cv < 0.05:
        return "Excellent"
    elif mean_c > 0.80 and cv < 0.10:
        return "Good"
    elif mean_c > 0.70 and cv < 0.15:
        return "Fair"
    else:
        return "Poor"
