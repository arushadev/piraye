"""This module includes Tokenizer class for tokenizing texts"""
from abc import ABC
from typing import List, Tuple

import nltk
from nltk import NLTKWordTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer

from ...tokenizer import Tokenizer


class NltkTokenizer(Tokenizer, ABC):
    """
    A class impl tokenizer with nltk
    ...
    Methods
    -------
    word_tokenize(text: str):
        return tokenized text
    sentence_tokenize(text: str):
        return sentence tokenized text
    """

    def __init__(self):
        """
        constructor
        """
        super().__init__()
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("downloading tokenizer data : ")
            nltk.download('punkt')
        self.__tokenizer = NLTKWordTokenizer()
        self.__sentence_tokenize = PunktSentenceTokenizer()

    def word_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = self._clean_text(text)
        spans = self.__tokenizer.span_tokenize(text2)
        return [(span[0], span[1], text[span[0]:span[1]]) for span in spans]

    def sentence_span_tokenize(self, text, clean_before_tokenize=True) -> List[Tuple[int, int, str]]:
        text2 = self._clean_text(text) if clean_before_tokenize else text
        spans = self.__sentence_tokenize.span_tokenize(text2)
        return [(span[0], span[1], text[span[0]:span[1]]) for span in spans]
