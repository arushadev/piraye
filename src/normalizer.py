"""This module includes Normalizer class for normalizing texts"""
from __future__ import annotations

from typing import List

from .char_config import CharConfig
from .mappings import MappingDict
from .nltk_tokenizer import NltkTokenizer, Tokenizer


# pylint: disable=too-few-public-methods
class Normalizer:
    """
    A class for normalizer.

    ...

    Attributes
    ----------
    configs : List[str]
        list of desired configs
    remove_extra_spaces : bool
        that determines spaces stick together or not
    tokenization : bool
        tokenize text or not


    Methods
    -------
    normalize(text: str):
        get a text and normalize it and finally return it
    """

    def __init__(self, configs=None, remove_extra_spaces: bool = True, tokenization: bool = True,
                 tokenizer: Tokenizer = None):
        """
            constructor
            :param  configs : List[str]
                list of desired configs
            :param  remove_extra_spaces : bool
                that determines spaces stick together or not
            :param  tokenization : bool
                tokenize text or not
        """
        # Create a blank Tokenizer with just the English vocab
        if configs is None:
            configs = []
        self.__configs = configs
        self.__remove_extra_spaces = remove_extra_spaces
        self.__mapping = MappingDict.load_jsons(self.__configs)

        if tokenization:
            if tokenizer:
                self.__tokenizer = tokenizer
            else:
                self.__tokenizer = NltkTokenizer()
        else:
            self.__tokenizer = None

    # pylint: disable=too-many-branches
    def normalize(self, text: str) -> str:
        """
            return a normalized text
            :param text: the input text
            :return: normalized text
        """

        if self.__tokenizer:
            is_token_list = self.__tokenize(text)
        else:
            is_token_list = [True] * len(text)
        result = ""
        last = None
        for i, char in enumerate(text):
            is_token = is_token_list[i]
            mapping_char = self.__mapping.get(char)
            if not self.__remove_extra_spaces:
                if mapping_char and \
                        (not mapping_char.is_token or (mapping_char.is_token and is_token)):
                    char = mapping_char.char
                result += char
            else:
                current = mapping_char if mapping_char else CharConfig(char)
                if current.is_space:
                    if last is None:
                        last = current
                    elif not last.is_space and last.space_after is not False:
                        last = current
                    elif last.is_space and current.space_priority < last.space_priority:
                        last = current
                else:
                    if last and last.is_space and last.space_before is not False:
                        result += last.char
                    # If last char is not space and need space before current or after last
                    if last and last.is_space is not True and \
                            (current.space_before or last.space_after) and is_token:
                        result += " "
                    if not current.is_token or (current.is_token and is_token):
                        result += current.char
                    else:
                        result += char
                    last = current
        if last and last.is_space:
            result += last.char
        return result

    def __tokenize(self, text: str) -> List[bool]:
        """
            return list of boolean that specifies each character is token or not
            :param text: the input text
            :return: list boolean.
        """
        is_token_list = [False] * len(text)
        tokens = self.__tokenizer.word_tokenize(text)
        text_counter = 0
        for token in tokens:
            token_index = text.index(token, text_counter)
            if len(token) == 1:
                is_token_list[token_index] = True
            text_counter = token_index + len(token)
        return is_token_list
