"""This module includes a Tokenizer class for tokenizing texts"""
from abc import ABC
from typing import List, Tuple

from spacy.lang.en import English
from spacy.pipeline import Sentencizer

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

    def __init__(self):
        """
        constructor
        """
        super().__init__()
        self.__nlp = English()
        self.__tokenizer = self.__nlp.tokenizer
        self.__sentencizer = Sentencizer()

    def word_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = self._clean_text(text)
        spans = self.__tokenizer(text2)
        return [(span.idx, span.idx + len(span.text), text[span.idx: span.idx + len(span.text)]) for span in spans]

    def sentence_span_tokenize(self, text, clean_before_tokenize=True) -> List[Tuple[int, int, str]]:
        text2 = self._clean_text(text) if clean_before_tokenize else text
        spans = self.__sentencizer(self.__nlp(text2))
        result = []
        last_index = 0
        for span in spans:
            if span.is_sent_end:
                result.append((last_index, span.idx + len(span.text), text[last_index:span.idx + len(span.text)]))
                last_index = span.idx + len(span.text)
        return result
