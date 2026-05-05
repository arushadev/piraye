"""NLTK-based tokenizer implementations."""
from abc import ABC
from typing import List

import nltk
from nltk import NLTKWordTokenizer
from nltk.tokenize.api import TokenizerI
from nltk.tokenize.punkt import PunktSentenceTokenizer

from ..base_tokenizer import Tokenizer
from ..token import Token


# pylint: disable=too-few-public-methods
class NltkTokenizer(Tokenizer, ABC):
    """
    Base class for NLTK-based impl.

    This abstract class provides common functionality for impl
    that use the NLTK library for natural language processing.
    It ensures that required NLTK data is downloaded.
    """

    def __init__(self, tokenizer: TokenizerI, clean_before_tokenize=True):
        Tokenizer.__init__(self)
        try:
            nltk.data.find('impl/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer data...")
            nltk.download('punkt')
        self.__tokenizer = tokenizer
        self.__clean_before_tokenize = clean_before_tokenize

    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize text into words using NLTK.

        Args:
            text: Input text to tokenize

        Returns:
            List of Token objects representing words
        """
        if self.__clean_before_tokenize:
            text = self._clean_text(text)
        spans = self.__tokenizer.span_tokenize(text)
        tokens = [
            Token(
                content=text[span[0]:span[1]],
                position=(span[0], span[1]),
                type=self.__class__.__name__,
                sub_tokens=[]
            )
            for span in spans
        ]
        return tokens


class NltkWordTokenizer(NltkTokenizer):
    """
    Word tokenizer using NLTK's word tokenization algorithm.

    This tokenizer splits text into individual words and punctuation marks
    using NLTK's built-in word tokenizer.
    """

    def __init__(self, clean_before_tokenize=True):
        NltkTokenizer.__init__(self, NLTKWordTokenizer(), clean_before_tokenize)


class NltkSentenceTokenizer(NltkTokenizer):
    """
    Sentence tokenizer using NLTK's Punkt sentence tokenizer.

    This tokenizer splits text into sentences using NLTK's
    unsupervised sentence boundary detection algorithm.
    """

    def __init__(self, clean_before_tokenize=True):
        NltkTokenizer.__init__(self, PunktSentenceTokenizer(), clean_before_tokenize)
        self.__sentence_tokenize = PunktSentenceTokenizer()
