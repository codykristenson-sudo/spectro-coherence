"""
Tests for C-Index core calculations

Run with: pytest tests/
"""

import numpy as np
import pytest
from spectro_coherence.cindex import (
    calculate_c_index,
    c_index_statistics,
    detect_anomalies,
    coherence_quality_score
)


def test_calculate_c_index_basic():
    """Test C-Index calculation on synthetic data."""
    # Create smooth synthetic spectrum
    x = np.linspace(0, 10, 1000)
    flux = np.sin(x) + 1.0  # Smooth sinusoidal
    
    positions, c_indices = calculate_c_index(flux, window=100, step=50)
    
    # Check output shapes
    assert len(positions) == len(c_indices)
    assert len(c_indices) > 0
    
    # Check C-Index range [0, 1]
    assert np.all(c_indices >= 0)
    assert np.all(c_indices <= 1)
    
    # Smooth data should have high coherence
    assert np.mean(c_indices) > 0.7


def test_calculate_c_index_noisy():
    """Test C-Index on noisy data."""
    # Create noisy spectrum
    np.random.seed(42)
    flux = np.random.normal(1.0, 0.5, 1000)
    
    positions, c_indices = calculate_c_index(flux, window=100, step=50)
    
    # Noisy data should have lower coherence than smooth
    assert np.mean(c_indices) < 0.9


def test_calculate_c_index_with_nans():
    """Test C-Index handles NaN values."""
    flux = np.ones(1000)
    flux[100:110] = np.nan  # Add some NaNs
    
    positions, c_indices = calculate_c_index(flux, window=100, step=50)
    
    # Should skip windows with too many NaNs but still return results
    assert len(c_indices) > 0
    assert np.all(np.isfinite(c_indices))


def test_c_index_statistics():
    """Test statistics calculation."""
    c_indices = np.array([0.85, 0.87, 0.89, 0.86, 0.88])
    
    stats = c_index_statistics(c_indices)
    
    assert 'mean' in stats
    assert 'std' in stats
    assert 'min' in stats
    assert 'max' in stats
    assert 'cv' in stats
    assert 'anomaly_threshold' in stats
    
    assert stats['mean'] == pytest.approx(0.87, abs=0.01)
    assert stats['min'] == 0.85
    assert stats['max'] == 0.89


def test_detect_anomalies():
    """Test anomaly detection."""
    positions = np.array([10, 20, 30, 40, 50])
    c_indices = np.array([0.85, 0.87, 0.60, 0.86, 0.88])  # One anomaly
    
    anomaly_pos, anomaly_vals = detect_anomalies(positions, c_indices, threshold_sigma=2.0)
    
    # Should detect the 0.60 value as anomaly
    assert len(anomaly_pos) > 0
    assert 0.60 in anomaly_vals


def test_coherence_quality_score():
    """Test quality score assignment."""
    # Excellent quality
    assert coherence_quality_score(0.90, 0.03) == "Excellent"
    
    # Good quality
    assert coherence_quality_score(0.85, 0.07) == "Good"
    
    # Fair quality
    assert coherence_quality_score(0.75, 0.12) == "Fair"
    
    # Poor quality
    assert coherence_quality_score(0.65, 0.20) == "Poor"


def test_c_index_edge_cases():
    """Test edge cases."""
    # Very short array
    flux = np.ones(50)
    positions, c_indices = calculate_c_index(flux, window=100, step=50)
    assert len(c_indices) == 0  # Window larger than data
    
    # All NaN
    flux = np.full(1000, np.nan)
    positions, c_indices = calculate_c_index(flux, window=100, step=50)
    assert len(c_indices) == 0
    
    # Constant flux (perfect stability)
    flux = np.ones(1000)
    positions, c_indices = calculate_c_index(flux, window=100, step=50)
    assert len(c_indices) > 0
    assert np.all(c_indices > 0.8)  # Should have high coherence


def test_c_index_reproducibility():
    """Test that C-Index calculation is deterministic."""
    np.random.seed(42)
    flux = np.random.normal(1.0, 0.1, 1000)
    
    pos1, c1 = calculate_c_index(flux, window=100, step=50)
    pos2, c2 = calculate_c_index(flux, window=100, step=50)
    
    np.testing.assert_array_equal(pos1, pos2)
    np.testing.assert_array_equal(c1, c2)
