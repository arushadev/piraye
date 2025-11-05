"""Spacy-based tokenizer implementations."""
from abc import ABC
from typing import List

from spacy.lang.en import English  # pylint: disable=import-error
from spacy.pipeline import Sentencizer  # pylint: disable=import-error

from ..token import Token
from .base_tokenizer import Tokenizer


# pylint: disable=too-few-public-methods
class SpacyTokenizer(Tokenizer, ABC):
    """
    Base class for Spacy-based tokenizers.

    This abstract class provides common functionality for tokenizers
    that use the Spacy library for natural language processing.
    """

    def __init__(self):
        Tokenizer.__init__(self)
        self._nlp = English()


class SpacyWordTokenizer(SpacyTokenizer):
    """
    Word tokenizer using Spacy's tokenization algorithm.

    This tokenizer splits text into individual words and punctuation marks
    using Spacy's built-in tokenizer.
    """

    def __init__(self):
        SpacyTokenizer.__init__(self)
        self.__tokenizer = self._nlp.tokenizer

    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize text into words using Spacy.

        Args:
            text: Input text to tokenize

        Returns:
            List of Token objects representing words
        """
        text2 = self._clean_text(text)
        spans = self.__tokenizer(text2)
        tokens = [
            Token(
                content=text[span.idx:span.idx + len(span.text) + 1],
                position=(span.idx, span.idx + len(span.text) + 1),
                type="SpacyWordTokenizer",
                sub_tokens=[]
            )
            for span in spans
        ]
        return tokens


class SpacySentenceTokenizer(SpacyTokenizer):
    """
    Sentence tokenizer using Spacy's Sentencizer.

    This tokenizer splits text into sentences using Spacy's
    rule-based sentence boundary detection.
    """

    def __init__(self):
        SpacyTokenizer.__init__(self)
        self.__sentencizer = Sentencizer()

    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize text into sentences using Spacy.

        Args:
            text: Input text to tokenize

        Returns:
            List of Token objects representing sentences
        """
        text2 = self._clean_text(text)
        spans = self.__sentencizer(self._nlp(text2))
        tokens = []
        last_index = 0

        for span in spans:
            if span.is_sent_end:
                start = last_index
                end = span.idx + len(span.text)
                tokens.append(
                    Token(
                        content=text[start:end],
                        position=(start, end),
                        type="SpacySentenceTokenizer",
                        sub_tokens=[]
                    )
                )
                last_index = span.idx + len(span.text)

        return tokens
