"""This module includes Normalizer class for normalizing texts"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class Normalizer(ABC):

    @abstractmethod
    def normalize(self, text: str) -> str:
        """
        Normalize the input text.
        :param text: The input text to normalize.
        :return: The normalized text.
        """
        pass

    @abstractmethod
    def span_normalize(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Normalize the input text and return spans of normalized tokens.
        :param text: The input text to normalize.
        :return: A list of tuples containing the start index, end index, and normalized token for each token span.
        """
        pass
