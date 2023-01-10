"""This module includes Tokenizer class for tokenizing texts"""
from typing import List, Tuple

import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer

from .mappings import MappingDict
from .tokenizer import Tokenizer


class NltkTokenizer(Tokenizer):
    """
    A class for nltk tokenizing.
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
        self.__tokenizer = TreebankWordTokenizer()
        self.__sentence_tokenize = PunktSentenceTokenizer()

    def word_tokenize(self, text) -> List[str]:
        tokens = self.word_span_tokenize(text)
        return [text for (_, _, text) in tokens]

    def word_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        spans = self.__tokenizer.span_tokenize(text2)
        return [(span[0], span[1], text[span[0]:span[1]]) for span in spans]

    def sentence_tokenize(self, text) -> List[str]:
        tokens = self.sentence_span_tokenize(text)
        return [text for (_, _, text) in tokens]

    def sentence_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        spans = self.__sentence_tokenize.span_tokenize(text2)
        return [(span[0], span[1], text[span[0]:span[1]]) for span in spans]
