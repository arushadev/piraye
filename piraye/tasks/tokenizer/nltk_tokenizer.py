"""This module includes Tokenizer class for tokenizing texts"""
from abc import ABC
from typing import List, Tuple

import nltk
from nltk import NLTKWordTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer

from ..normalizer.mappings import MappingDict
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

    def __init__(self, ):
        """
        constructor
        """
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("downloading tokenizer data : ")
            nltk.download('punkt')
        self.__en_mapping = MappingDict.load_jsons(["digit_en", "punc_en"])
        self.__tokenizer = NLTKWordTokenizer()
        self.__sentence_tokenize = PunktSentenceTokenizer()

    def word_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = self.__clean_text(text)
        spans = self.__tokenizer.span_tokenize(text2)
        return [(span[0], span[1], text[span[0]:span[1]]) for span in spans]

    def sentence_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = self.__clean_text(text)
        spans = self.__sentence_tokenize.span_tokenize(text2)
        return [(span[0], span[1], text[span[0]:span[1]]) for span in spans]

    def __clean_text(self, text: str) -> str:
        """
        Clean the input text by replacing digits and punctuation with normalized versions.
        :param text: he input text to clean.
        :return: The cleaned text with normalized digits and punctuation.
        """
        return ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
