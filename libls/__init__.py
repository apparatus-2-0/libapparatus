"""Initialization file for the libls package."""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    print(f'Package {__name__} not found. Please install it using pip.')

# Initialise main.py
from .main import *
