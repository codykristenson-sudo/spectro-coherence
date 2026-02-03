#!/usr/bin/env python3
"""
spectro-coherence: Coherence Analysis for Astronomical Spectroscopy
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="spectro-coherence",
    version="1.0.0",
    author="Cody A. Kristenson",
    author_email="",  # Add if desired
    description="C-Index coherence analysis for spectroscopic data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodyKristenson/spectro-coherence",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
        "astropy>=4.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12",
        ]
    },
    entry_points={
        "console_scripts": [
            "spectro-coherence=examples.winered_analysis:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
