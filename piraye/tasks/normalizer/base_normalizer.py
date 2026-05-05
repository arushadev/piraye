"""This module includes Normalizer class for normalizing texts"""

from abc import ABC, abstractmethod

from .normalized_text import NormalizedText


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
    def normalize(self, text: str) -> tuple[str, NormalizedText]:
        """
        Normalize the input text.
        Args:
            text: The input text to normalize.
        Returns:
            A tuple containing:
                - The normalized text
                - NormalizationResult with shifts and punctuation locations
        """