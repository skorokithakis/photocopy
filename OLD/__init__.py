"""
Copy your photos from an SD card or camera to a specific directory.
"""

from .version import VERSION, __version__
try:
    from .photocopy import main
except ImportError:
    # This may raise an error when importing version to install.
    pass
