"""
NormalizationResult data class for text normalization metadata.

This module provides the NormalizationResult class which encapsulates
the results and metadata from text normalization operations.
"""
from dataclasses import dataclass, field


@dataclass
class NormalizationResult:
    """
    Result of text normalization containing metadata about the normalization process.

    Attributes:
        shifts: List of tuples (position, shift) tracking character position changes
                during normalization for mapping back to original text
        punc_positions: List of punctuation locations in the normalized text
    """
    shifts: list[tuple[int, int]] = field(default_factory=list)
    punc_positions: list[int] = field(default_factory=list)
