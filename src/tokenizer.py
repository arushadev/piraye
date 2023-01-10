"""Base class of tokenizer"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class Tokenizer(ABC):
    """
    Abstract class for tokenizing
    ...


    Methods
    -------
    word_tokenize(text: str):
        return tokenized text (abstract method)
    sentence_tokenize(text: str):
        return sentence tokenized text (abstract method)
    """

    @abstractmethod
    def word_tokenize(self, text) -> List[str]:
        """
        Return a tokenized text.
        :param text: the input text
        :return: list of words
        """

    @abstractmethod
    def word_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        """
        Return spans of tokenized text.
        :param text: the input text
        :return: list of token spans in text
        """

    @abstractmethod
    def sentence_tokenize(self, text) -> List[str]:
        """
        Return a sentence tokenized text.
        :param text: the input text
        :return: list of sentences
        """

    @abstractmethod
    def sentence_span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        """
        Return spans of tokenized text.
        :param text: the input text
        :return: list of token spans in text
        """
