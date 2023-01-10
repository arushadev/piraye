"""This module includes Tokenizer class for tokenizing texts"""

from abc import ABC, abstractmethod
from typing import List, Tuple

from typing import List, Tuple

import nltk
from nltk import TreebankWordTokenizer, sent_tokenize

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

    def word_tokenize(self, text) -> List[str]:
        """
            Return a tokenized text.
            :param text: the input text
            :return: list of words
        """
        tokens_en = self.span_tokenize(text)
        return [text[a:b] for (a, b) in tokens_en]

    def span_tokenize(self, text) -> List[Tuple[int, int]]:
        """
            Return span of tokens
            :param text: the input text
            :return: list of spans
        """
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        return self.__tokenizer.span_tokenize(text2)

    def sentence_tokenize(self, text):
        """
            Return a sentence tokenized text.
            :param text: the input text
            :return: list of sentences
        """
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        spans = PunktSentenceTokenizer().span_tokenize(text2)
        return [text[span[0]:span[1]] for span in spans]

    def sentence_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        """
            Return a sentence tokenized text.
            :param text: the input text
            :return: list of sentences
        """
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        spans = PunktSentenceTokenizer().span_tokenize(text2)
        return [(span[0], span[1], text[span[0]:span[1]]) for span in spans]
