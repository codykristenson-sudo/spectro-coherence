# spectro-coherence

Coherence analysis for astronomical spectroscopy using the C-Index (Coherence Index) framework.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

## What It Does

**spectro-coherence** provides quantitative quality metrics for spectroscopic data through coherence analysis:

- Calculates C-Index (Coherence Index) for spectroscopic flux arrays
- Generates quality assessment metrics beyond traditional SNR
- Produces publication-quality visualizations
- Works with FITS format spectroscopy (generic and WINERED-specific loaders)
- Detects coherence anomalies and localized quality issues

## What It Doesn't Do

This is **stewardship-mode software** with clearly defined scope:

- ❌ Advanced statistical modeling or machine learning
- ❌ Spectral line fitting or equivalent width measurements
- ❌ Telluric correction or flux calibration
- ❌ GUI or interactive applications
- ❌ Custom feature requests for specific use cases

**If you need different functionality, fork the repository.** That's what open source is for.

## Installation

### From PyPI (when available)
```bash
pip install spectro-coherence
```

### From Source
```bash
git clone https://github.com/CodyKristenson/spectro-coherence.git
cd spectro-coherence
pip install -e .
```

### Requirements
- Python ≥ 3.8
- numpy ≥ 1.20
- scipy ≥ 1.7
- matplotlib ≥ 3.3
- astropy ≥ 4.3

## Quick Start

### Python API
```python
from spectro_coherence import load_fits_spectrum, calculate_c_index

# Load spectrum
spectrum = load_fits_spectrum('spectrum.fits')

# Calculate C-Index
positions, c_indices = calculate_c_index(spectrum.flux, window=200, step=100)

# Get statistics
from spectro_coherence import c_index_statistics
stats = c_index_statistics(c_indices)
print(f"Mean coherence: {stats['mean']:.4f} ± {stats['std']:.4f}")
```

### Command Line (WINERED Example)
```bash
# Analyze single spectrum
python examples/winered_analysis.py spectrum.fits --output ./results

# Analyze directory of spectra
python examples/winered_analysis.py /path/to/spectra --output ./results
```

## The C-Index Framework

C-Index quantifies spectral coherence through three components:

1. **Smoothness**: Inverse of normalized gradient magnitude
2. **Stability**: Inverse coefficient of variation  
3. **Consistency**: Normalized autocorrelation (lag-1)

Combined: `C = (Smoothness + Stability + Consistency) / 3`

Range: [0, 1] where 1 represents perfect coherence

### Applications

- **Quality Control**: Pipeline validation and optimization
- **Regional Assessment**: Identify problematic spectral regions
- **Comparative Analysis**: Quality-match spectra for differential studies
- **Anomaly Detection**: Flag regions with degraded coherence

## Examples

See `examples/` directory:
- `winered_analysis.py`: Complete WINERED data analysis workflow

## Documentation

Detailed API documentation and methodology in `docs/` (when available).

Framework background: [Kristenson, C.A. (2024-2026). EOS Framework Series. Zenodo.](https://zenodo.org/communities/eos-framework)

## Citation

If you use this software in your research, please cite:

```bibtex
@software{kristenson2026spectrocoherence,
  author       = {Kristenson, Cody A.},
  title        = {spectro-coherence: Coherence Analysis for Spectroscopy},
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://github.com/CodyKristenson/spectro-coherence}
}
```

And reference the underlying framework:
```bibtex
@misc{kristenson2024eos,
  author       = {Kristenson, Cody A.},
  title        = {Emergent Order Systems (EOS) Framework Series},
  year         = {2024-2026},
  publisher    = {Zenodo},
  url          = {https://zenodo.org/communities/eos-framework}
}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**TL;DR**: This software is in maintenance mode. Bug fixes and documentation improvements welcome. Major feature requests will likely be declined to maintain focus.

## Maintenance

This is **stewardship-mode software**:
- **Active**: Bug fixes, compatibility updates, documentation
- **Inactive**: New features, scope expansion, custom requests

Issues reviewed monthly. Response time may vary based on maintainer availability.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

For framework-related questions or collaboration inquiries, see contact information in the Zenodo publications.

For software bugs or issues, use the GitHub issue tracker.

---

**Developed by:** Cody A. Kristenson, Independent Researcher  
**Location:** West Fargo, North Dakota, USA  
**Background:** 19 years manufacturing quality assurance
