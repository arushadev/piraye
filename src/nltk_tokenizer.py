"""This module includes Tokenizer class for tokenizing texts"""

from abc import ABC, abstractmethod
from typing import List

import nltk
from nltk import word_tokenize, sent_tokenize

from .mappings import MappingDict


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
    def sentence_tokenize(self, text):
        """
            Return a sentence tokenized text.
            :param text: the input text
            :return: list of sentences
        """


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

    def word_tokenize(self, text) -> List[str]:
        """
            Return a tokenized text.
            :param text: the input text
            :return: list of words
        """
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        tokens_en = word_tokenize(text2)
        return NltkTokenizer.__get_original_tokens(text, text2, tokens_en)

    def sentence_tokenize(self, text):
        """
            Return a sentence tokenized text.
            :param text: the input text
            :return: list of sentences
        """
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        tokens_en = sent_tokenize(text2)
        return NltkTokenizer.__get_original_tokens(text, text2, tokens_en)

    @staticmethod
    def __get_original_tokens(text: str, text2: str, tokens_en: List[str]) -> List[str]:
        text2_counter = 0
        tokens = []
        for token_en in tokens_en:
            try:
                token_index = text2.index(token_en, text2_counter)
                curr_text = text[token_index:token_index + len(token_en)]
                tokens.append(curr_text)
                text2_counter = token_index + len(token_en)
            except ValueError as error:
                if token_en in ('``', "''"):
                    while True:
                        curr_text = text[text2_counter:text2_counter + 1]
                        text2_counter = text2_counter + 1
                        if len(curr_text.strip()) > 0:
                            tokens.append(curr_text)
                            break
                else:
                    raise error
        return tokens
