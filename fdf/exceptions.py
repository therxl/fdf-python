class FdfError(Exception):
    """Base exception for all FdF-specific errors."""


class MapFormatError(FdfError):
    """Raised when the map file contents do not match the FDF format."""
