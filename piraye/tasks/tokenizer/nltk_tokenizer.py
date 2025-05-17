"""This module includes Tokenizer class for tokenizing texts"""
from abc import ABC
from typing import List

import nltk
from nltk import NLTKWordTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer

from .base_tokenizer import Tokenizer
from .token import Token


class NltkTokenizer(Tokenizer, ABC):
    """
    A class impl tokenizer with nltk
    ...
    Methods
    -------
    tokenize(text: str):
        return tokenized text
    """

    def __init__(self):
        Tokenizer.__init__(self)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("downloading tokenizer data : ")
            nltk.download('punkt')


class NltkWordTokenizer(NltkTokenizer):
    def __init__(self):
        NltkTokenizer.__init__(self)
        self.__tokenizer = NLTKWordTokenizer()

    def tokenize(self, text) -> List[Token]:
        text2 = self._clean_text(text)
        spans = self.__tokenizer.span_tokenize(text2)
        tokens = [
            Token(content=text[span[0]:span[1]], position=(span[0], span[1]), type="NltkWordTokenizer", sub_tokens=[])
            for span in spans]
        return tokens


class NltkSentenceTokenizer(NltkTokenizer):
    def __init__(self):
        NltkTokenizer.__init__(self)
        self.__sentence_tokenize = PunktSentenceTokenizer()

    def tokenize(self, text, clean_before_tokenize=True) -> List[Token]:
        text2 = self._clean_text(text) if clean_before_tokenize else text
        spans = self.__sentence_tokenize.span_tokenize(text2)
        tokens = [Token(content=text[span[0]:span[1]], position=(span[0], span[1]), type="NltkSentenceTokenizer",
                        sub_tokens=[]) for span in spans]
        return tokens
