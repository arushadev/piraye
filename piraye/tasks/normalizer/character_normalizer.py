"""This module includes Normalizer class for normalizing texts"""
from __future__ import annotations

from abc import ABC
from typing import List, Tuple

from .char_config import CharConfig
from .mappings import MappingDict
from ..tokenizer.nltk_tokenizer import NltkTokenizer
from ...tokenizer import Tokenizer
from ...normalizer import Normalizer


# pylint: disable=too-few-public-methods
class CharacterNormalizer(Normalizer, ABC):
    """
    Impl normalizer by character level normalization
    Attributes
    ----------
    config (List[str]): list of desired configs
    remove_extra_spaces (bool): that determines spaces stick together or not
    tokenization (bool): Whether to tokenize the text before normalization.
    """

    def __init__(self, configs=None, remove_extra_spaces: bool = True, tokenization: bool = True,
                 tokenizer: Tokenizer = None):
        """
        Constructor for NormalizerBuilder.
        :param configs: List of normalizer configs to initialize with.
        :param remove_extra_spaces: Whether to remove extra spaces during normalization.
        :param tokenization: Whether to tokenize the text before normalization.
        :param tokenizer: Tokenizer algorithm (Default is NltkTokenizer)
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
            returns a normalized text
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
            returns a list of booleans that specifies each character is token or not
            :param text: the input text
            :return: list boolean.
        """
        is_token_list = [False] * len(text)
        spans = self.__tokenizer.word_span_tokenize(text)
        for (start, end, _) in spans:
            if start + 1 == end:
                is_token_list[start] = True
        return is_token_list

    def span_normalize(self, text: str) -> List[Tuple[int, int, str]]:
        raise NotImplementedError()
