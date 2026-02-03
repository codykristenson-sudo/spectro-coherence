# Contributing to spectro-coherence

Thank you for your interest in contributing!

## Maintenance Philosophy

**This software is in stewardship mode.** The underlying C-Index framework is published, validated, and stable. This package provides access to that framework — it does not expand it.

## What I Will Accept

### ✅ Bug Fixes
- Calculation errors
- FITS loading issues
- Compatibility problems
- Documentation errors

**Please include:**
- Clear description of the bug
- Minimal reproduction example
- Test case demonstrating the fix

### ✅ Documentation Improvements
- Clarifications
- Additional examples
- Usage guides
- Docstring corrections

### ✅ FITS Format Support
- Additional spectroscopic format loaders
- Must maintain same SpectrumFITS interface
- Include example data or clear documentation

### ✅ Performance Improvements
- Optimizations that don't change results
- Must include benchmarks showing improvement
- Cannot add new dependencies

## What I Won't Accept

### ❌ New Analysis Methods
The C-Index framework is defined and published. If you need different coherence metrics, **fork the repository** and develop your own variant.

### ❌ Feature Creep
- Machine learning integration
- Advanced statistical modeling
- Interactive GUIs
- Database backends
- Cloud deployment tools

**Why?** Scope creep kills maintainability. This package does one thing well.

### ❌ Major Architectural Changes
The codebase is intentionally simple. I won't accept refactors that add complexity without clear necessity.

### ❌ Framework Modifications
The C-Index calculation in `cindex.py` implements published methodology. Changes to the algorithm itself require peer review and publication — that happens in papers, not PRs.

## How to Contribute

### For Bug Fixes

1. Open an issue describing the bug
2. Wait for confirmation (I review monthly)
3. Fork and create a branch
4. Fix the bug with tests
5. Submit PR referencing the issue

### For Documentation

1. Fork the repository
2. Make your improvements
3. Submit PR with clear description

### For FITS Format Support

1. Open an issue with format details
2. Provide example data or documentation
3. Fork and implement loader
4. Submit PR with tests and examples

## Response Time

I review issues and PRs **monthly**. I have a full-time manufacturing job and this is side work. 

**Please be patient.** If you need faster turnaround, consider:
- Forking for your own use
- Hiring a developer
- Finding community contributors

## Code Standards

- Python ≥ 3.8 compatibility
- PEP 8 style (use `black` if available)
- Docstrings for public functions
- Type hints where helpful
- Tests for new code

## Testing

Run existing tests:
```bash
pytest tests/
```

Add tests for bug fixes:
```python
def test_your_bugfix():
    # Demonstrate the bug is fixed
    result = function_that_was_broken()
    assert result == expected_value
```

## Questions?

- **Software bugs**: GitHub issues
- **Framework questions**: See Zenodo publications
- **Collaboration**: Contact info in Zenodo profile

## The Bottom Line

This is **maintenance-mode software** for a **published framework**. 

I welcome contributions that improve quality, usability, and compatibility. I will decline contributions that expand scope, add complexity, or require ongoing maintenance burden.

**If this doesn't meet your needs, please fork it!** That's what open source is for, and I won't be offended.

Thank you for understanding.

— Cody
