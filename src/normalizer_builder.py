"""This module is for config set """
from __future__ import annotations

import enum

from .normalizer import Normalizer


class Config(enum.Enum):
    """
    List of all available configs in this normalizer
    """
    ALPHABET_AR = "alphabet_ar"
    ALPHABET_EN = "alphabet_en"
    ALPHABET_FA = "alphabet_fa"
    DIGIT_AR = "digit_ar"
    DIGIT_EN = "digit_en"
    DIGIT_FA = "digit_fa"
    DIACRITIC_DELETE = "diacritic_delete"
    SPACE_DELETE = "space_delete"
    SPACE_NORMAL = "space_normal"
    SPACE_KEEP = "space_keep"
    PUNCTUATION_AR = "punc_ar"
    PUNCTUATION_FA = "punc_fa"
    PUNCTUATION_EN = "punc_en"


class NormalizerBuilder:
    """
    A class for normalizer configs.
    ...

    Attributes
    ----------
    __configs : List[str] or List[Config]
        list of desired configs
    __remove_extra_spaces : bool
        that determines spaces stick together or not
    __tokenization : bool
        tokenize text or not

    Methods
    -------
    build():
        build an instance of normalizer with current config
    """

    def __init__(self, configs=None,
                 remove_extra_spaces: bool = False,
                 tokenization: bool = False):
        """
            constructor
            :param configs
        """
        if configs is None:
            configs = []
        self.__configs = configs
        self.__remove_extra_spaces = remove_extra_spaces
        self.__tokenization = tokenization

    def build(self) -> Normalizer:
        """
            Helper function for adding configs
        """
        if self.__remove_extra_spaces and \
                not (Config.SPACE_DELETE in self.__configs or
                     Config.SPACE_KEEP in self.__configs or
                     Config.SPACE_NORMAL in self.__configs):
            self.__configs.append(Config.SPACE_KEEP)
        return Normalizer([c.value for c in self.__configs],
                          self.__remove_extra_spaces, self.__tokenization)

    def alphabet_ar(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.ALPHABET_AR)
        return self

    def alphabet_en(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.ALPHABET_EN)
        return self

    def alphabet_fa(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.ALPHABET_FA)
        return self

    def digit_ar(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.ALPHABET_AR)
        return self

    def digit_en(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.DIGIT_EN)
        return self

    def digit_fa(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.DIGIT_FA)
        return self

    def diacritic_delete(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.DIACRITIC_DELETE)
        return self

    def space_delete(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.SPACE_DELETE)
        return self

    def space_normal(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.SPACE_NORMAL)
        return self

    def space_keep(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.SPACE_KEEP)
        return self

    def punctuation_ar(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.PUNCTUATION_AR)
        return self

    def punctuation_fa(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.PUNCTUATION_FA)
        return self

    def punctuation_en(self) -> NormalizerBuilder:
        """
            Helper function for adding configs
        """
        self.__configs.append(Config.PUNCTUATION_EN)
        return self

    def remove_extra_spaces(self, remove_extra_spaces: bool = True) -> NormalizerBuilder:
        """
        Helper function for adding configs
        """
        self.__remove_extra_spaces = remove_extra_spaces
        return self

    def tokenizing(self, tokenization: bool = True) -> NormalizerBuilder:
        """
        Helper function for adding configs
        """
        self.__tokenization = tokenization
        return self
