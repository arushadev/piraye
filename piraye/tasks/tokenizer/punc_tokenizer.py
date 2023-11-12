"""This module includes Tokenizer class for tokenizing texts"""
from abc import ABC
from typing import List, Tuple

from ...tokenizer import Tokenizer


class PuncTokenizer(Tokenizer, ABC):
    """
    A class impl tokenizer with punctuation restoration and then tokenize it
    """

    def word_span_tokenize(self, text: str) -> List[Tuple[int, int, str]]:
        pass

    def sentence_span_tokenize(self, text: str) -> List[Tuple[int, int, str]]:
        pass
