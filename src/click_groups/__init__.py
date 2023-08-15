"""Enable grouping and ordering of commands."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("click-groups")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Lukasz G. Migas"
__email__ = "lukas.migas@yahoo.com"
