"""NLTK-based tokenizer implementations."""
from abc import ABC
from typing import List

import nltk
from nltk import NLTKWordTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer

from .base_tokenizer import Tokenizer
from ..token import Token


# pylint: disable=too-few-public-methods
class NltkTokenizer(Tokenizer, ABC):
    """
    Base class for NLTK-based tokenizers.

    This abstract class provides common functionality for tokenizers
    that use the NLTK library for natural language processing.
    It ensures that required NLTK data is downloaded.
    """

    def __init__(self):
        Tokenizer.__init__(self)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer data...")
            nltk.download('punkt')


class NltkWordTokenizer(NltkTokenizer):
    """
    Word tokenizer using NLTK's word tokenization algorithm.

    This tokenizer splits text into individual words and punctuation marks
    using NLTK's built-in word tokenizer.
    """

    def __init__(self):
        NltkTokenizer.__init__(self)
        self.__tokenizer = NLTKWordTokenizer()

    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize text into words using NLTK.

        Args:
            text: Input text to tokenize

        Returns:
            List of Token objects representing words
        """
        text2 = self._clean_text(text)
        spans = self.__tokenizer.span_tokenize(text2)
        tokens = [
            Token(
                content=text[span[0]:span[1]],
                position=(span[0], span[1]),
                type="NltkWordTokenizer",
                sub_tokens=[]
            )
            for span in spans
        ]
        return tokens


class NltkSentenceTokenizer(NltkTokenizer):
    """
    Sentence tokenizer using NLTK's Punkt sentence tokenizer.

    This tokenizer splits text into sentences using NLTK's
    unsupervised sentence boundary detection algorithm.
    """

    def __init__(self):
        NltkTokenizer.__init__(self)
        self.__sentence_tokenize = PunktSentenceTokenizer()

    def tokenize(self, text: str, clean_before_tokenize: bool = True) -> List[Token]:
        """
        Tokenize text into sentences using NLTK.

        Args:
            text: Input text to tokenize
            clean_before_tokenize: Whether to clean text before tokenization

        Returns:
            List of Token objects representing sentences
        """
        text2 = self._clean_text(text) if clean_before_tokenize else text
        spans = self.__sentence_tokenize.span_tokenize(text2)
        tokens = [
            Token(
                content=text[span[0]:span[1]],
                position=(span[0], span[1]),
                type="NltkSentenceTokenizer",
                sub_tokens=[])
            for span in spans]
        return tokens
