from .version import VERSION
try:
    from .photocopy import main
except ImportError:
    # This may raise an error when importing version to install.
    pass
