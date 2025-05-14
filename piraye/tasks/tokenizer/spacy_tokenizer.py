"""This module includes a Tokenizer class for tokenizing texts"""
from abc import ABC
from typing import List, Tuple

from spacy.lang.en import English
from spacy.pipeline import Sentencizer

from .token import Token
from .base_tokenizer import Tokenizer


class SpacyTokenizer(Tokenizer, ABC):
    """
    A class impl tokenizer with spacy
    ...
    Methods
    -------
    tokenize(text: str):
        return tokenized text
    """

    def __init__(self):
        Tokenizer.__init__(self)
        self.__nlp = English()


class SpacyWordTokenizer(SpacyTokenizer):
    def __init__(self):
        SpacyTokenizer.__init__(self)
        self.__tokenizer = self.__nlp.tokenizer

    def tokenize(self, text: str) -> List[Token]:
        text2 = self._clean_text(text)
        spans = self.__tokenizer(text2)
        tokens = [Token(content=text[span[0]:span[1]], position=(span[0], span[1]), type="SpacyWordTokenizer",
                        sub_tokens=[]) for span in spans]
        return tokens


class SpacySentenceTokenizer(SpacyTokenizer):
    def __init__(self):
        SpacyTokenizer.__init__(self)
        self.__sentencizer = Sentencizer()

    def tokenize(self, text: str) -> List[Token]:
        text2 = self._clean_text(text)
        spans = self.__sentencizer(self.__nlp(text2))
        tokens = []
        last_index = 0
        for span in spans:
            if span.is_sent_end:
                start = last_index
                end = span.idx + len(span.text)
                tokens.append(
                    Token(content=text[start:end], position=(start, end), type="SpacySentenceTokenizer", sub_tokens=[]))
                last_index = span.idx + len(span.text)
        return tokens
