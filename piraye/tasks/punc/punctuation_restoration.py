"""Base class of tokenizer"""
from abc import ABC
from typing import List, Tuple

from ...normalizer import Normalizer


class PunctuationRestoration(Normalizer, ABC):
    """
    Normalize text by restoring mission punctuation
    """

    def normalize(self, text: str) -> str:
        """
        returns a text with punctuation
        :param text: Input text without punctuation
        :return: The text with punctuation
        """
        from deepmultilingualpunctuation import PunctuationModel
        model = PunctuationModel(model = "final")
        result = model.restore_punctuation(text)
        return result
        

    def span_normalize(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Return spans of missed punctuations
        :param text: Input text without punctuation
        :return: A list of tuples containing the start index, end index, and punctuation token for each token span.
        """
        pass
