"""This module includes Normalizer class for normalizing texts"""

from abc import ABC, abstractmethod

from ..normalization_result import NormalizationResult


class Normalizer(ABC):
    """
    The Normalizer class is an abstract base class that defines the interface
    for text normalization. It provides two abstract methods: normalize() and
    span_normalize(), subclasses can implement which to perform specific
    normalization tasks.

    Example Usage

    # Create a subclass of Normalizer
    class MyNormalizer(Normalizer):

        Def normalize (self, text: str) -> str:
            # Implement the normalization logic here
            ...

        Def span_normalize(self, text: str) -> List[Tuple[int, int, str]]:
            # Implement the normalization logic and return spans of normalized tokens
            ...

    # Create an instance of the subclass
    normalizer = MyNormalizer()

    # Normalize a text
    normalized_text = normalizer.normalize("This is a sample text.")

    # Normalize a text and get spans of normalized tokens
    normalized_spans = normalizer.span_normalize("This is a sample text.")
    """

    @abstractmethod
    def normalize(self, text: str) -> tuple[str, NormalizationResult]:
        """
        Normalize the input text.
        Args:
            text: The input text to normalize.
        Returns:
            A tuple containing:
                - The normalized text
                - NormalizationResult with shifts and punctuation locations
        """

    # noinspection PyMethodMayBeStatic
    def calc_original_position(self, shifts: list[tuple[int, int]], position: int) -> int:
        """
        Calculate the original positions needed to normalize the input text.
        Args:
            shifts: shifts that has been calculated by normalizer
            position: position in normalized text
        Returns:
            The original integer position before normalizing input text.
        """
        final_shift = 0
        for start, shift in shifts:
            if position < start:
                break
            if position >= start:
                final_shift = shift
        return position + final_shift

    # noinspection PyMethodMayBeStatic
    def calc_original_positions(
            self, shifts: list[tuple[int, int]],
            positions: list[int]
    ) -> list[int]:
        """
        Calculate the original positions needed to normalize the input text.
        Args:
            shifts: shifts that has been calculated by normalizer.
            positions: sorted list of positions to be calculated.
        Returns:
            The list of original integer position before normalizing
            input text.
        """
        result = []
        pointer_on_shift = 0
        for i, current in enumerate(positions):
            last = positions[i - 1] if i > 0 else 0
            if current < last:
                raise ValueError("The position list is not sorted")
            while current > shifts[pointer_on_shift][0]:
                pointer_on_shift += 1
                if pointer_on_shift >= len(shifts):
                    pointer_on_shift = len(shifts) - 1
                    result.append(shifts[pointer_on_shift][1] + current)
                    break
            if current < shifts[pointer_on_shift][0]:
                if pointer_on_shift == 0:
                    result.append(0)
                else:
                    final_shift = shifts[pointer_on_shift - 1][1]
                    result.append(final_shift + current)
            elif current == shifts[pointer_on_shift][0]:
                final_shift = shifts[pointer_on_shift][1]
                result.append(final_shift + current)
        return result
