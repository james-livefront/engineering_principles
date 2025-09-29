"""
LEAP - Livefront Engineering Automated Principles

Shared module for accessing engineering principles, detection patterns,
enforcement specifications, and platform requirements.
"""

from .loaders import LeapLoader

__version__ = "1.0.0"
__all__ = ["LeapLoader"]
