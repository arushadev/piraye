"""
NormalizationResult data class for text normalization metadata.

This module provides the NormalizationResult class which encapsulates
the results and metadata from text normalization operations.
"""
from dataclasses import dataclass, field


@dataclass
class NormalizedText:
    """
    Result of text normalization containing metadata about the normalization process.

    Attributes:
        shifts: List of tuples (position, shift) tracking character position changes
                during normalization for mapping back to original text
        punc_positions: List of punctuation locations in the normalized text
    """
    text: str = ""
    shifts: list[tuple[int, int]] = field(default_factory=list)
    punc_positions: list[int] = field(default_factory=list)

    def calc_original_position(self, position: int) -> int:
        """
        Calculate the original positions needed to normalize the input text.
        Args:
            position: position in normalized text
        Returns:
            The original integer position before normalizing input text.
        """
        return sum(shift for pos, shift in self.shifts if pos <= position) + position

    def calc_original_positions(self, positions: list[int]) -> list[int]:
        """
        Calculate the original positions needed to normalize the input text.
        Args:
            positions: sorted list of positions to be calculated.
        Returns:
            The list of original integer position before normalizing
            input text.
        """
        result = []
        shifts_pointer = 0
        shifts_sum = 0
        for i, current in enumerate(positions):
            if current < (positions[i - 1] if i > 0 else 0):
                raise ValueError("The position list is not sorted")
            while shifts_pointer < len(self.shifts) and self.shifts[shifts_pointer][0] <= current:
                shifts_sum += self.shifts[shifts_pointer][1]
                shifts_pointer += 1
            result.append(current + shifts_sum)
        return result
