"""Base class of tokenizer"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class Tokenizer(ABC):
    """
    Abstract class for tokenizing
    """

    def word_tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into a list of words.
        :param text: The input text to tokenize.
        :return: A list of tokenized words.
        """
        tokens = self.word_span_tokenize(text)
        return [text for (_, _, text) in tokens]

    @abstractmethod
    def word_span_tokenize(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Tokenize the input text and return spans of the tokenized words.
        :param text: The input text to tokenize.
        :return: A list of tuples containing the start index, end index, and the tokenized word for each word span.
        """

    def sentence_tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into a list of sentences.
        :param text: The input text to tokenize.
        :return: A list of sentences.
        """
        tokens = self.sentence_span_tokenize(text)
        return [text for (_, _, text) in tokens]

    @abstractmethod
    def sentence_span_tokenize(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Tokenize the input text and return spans of the tokenized sentences.
        :param text: The input text to tokenize.
        :return: A list of tuples containing the start index, end index, and the sentence for each sentence span.
        """
