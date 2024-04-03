"""This module includes a Tokenizer class for tokenizing texts"""
from abc import ABC
from typing import List, Tuple
from spacy.lang.en import English
from spacy.pipeline import Sentencizer

from ..normalizer.mappings import MappingDict
from ...tokenizer import Tokenizer


class SpacyTokenizer(Tokenizer, ABC):
    """
    A class impl tokenizer with spacy
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
        self.__nlp = English()
        self.__en_mapping = MappingDict.load_jsons(["digit_en", "punc_en"])
        self.__tokenizer = self.__nlp.tokenizer
        self.__sentencizer = Sentencizer()

    def word_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = self.__clean_text(text)
        spans = self.__tokenizer(text2)
        return [(span.idx, span.idx + len(span.text), text[span.idx: span.idx + len(span.text)]) for span in spans]

    def sentence_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = self.__clean_text(text)
        spans = self.__sentencizer(self.__nlp(text2))
        result = []
        last_index = 0
        for span in spans:
            if span.is_sent_end:
                result.append((last_index, span.idx + len(span.text), text[last_index:span.idx + len(span.text)]))
                last_index = span.idx + len(span.text)
        return result

    def __clean_text(self, text: str) -> str:
        """
        Clean the input text by replacing digits and punctuation with normalized versions.
        :param text: He inputs text to clean.
        :return: The cleaned text with normalized digits and punctuation.
        """
        return ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
