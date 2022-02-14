"""This module is for config set """
from __future__ import annotations

import enum
from typing import List

import src


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


class NormalizerConfiguration:
    """
    A class for normalizer configs.
    ...

    Attributes
    ----------
    configs : List[str] or List[Config]
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

    def __init__(self, configs: List = None,
                 remove_extra_spaces: bool = False,
                 tokenization: bool = False):
        """
            constructor
            :param configs
        """
        self.configs = configs if configs else []
        self.configs = [config if isinstance(config, str) else config.value
                        for config in self.configs]
        self.remove_extra_spaces = remove_extra_spaces
        self.tokenization = tokenization

    def build(self) -> src.Normalizer:
        """
            Helper function for adding configs
        """
        return src.Normalizer(NormalizerConfiguration(self.configs,
                                                      self.remove_extra_spaces,
                                                      self.tokenization))

    def alphabet_ar(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "alphabet_ar"
        self.configs.append(config)
        return self

    def alphabet_en(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "alphabet_en"
        self.configs.append(config)
        return self

    def alphabet_fa(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "alphabet_fa"
        self.configs.append(config)
        return self

    def digit_ar(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "digit_ar"
        self.configs.append(config)
        return self

    def digit_en(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "digit_en"
        self.configs.append(config)
        return self

    def digit_fa(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "digit_fa"
        self.configs.append(config)
        return self

    def diacritic_delete(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "diacritic_delete"
        self.configs.append(config)
        return self

    def space_delete(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "space_delete"
        self.configs.append(config)
        return self

    def space_normal(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "space_normal"
        self.configs.append(config)
        return self

    def space_keep(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "space_keep"
        self.configs.append(config)
        return self

    def punctuation_ar(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "punc_ar"
        self.configs.append(config)
        return self

    def punctuation_fa(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "punc_fa"
        self.configs.append(config)
        return self

    def punctuation_en(self) -> NormalizerConfiguration:
        """
            Helper function for adding configs
        """
        config = "punc_en"
        self.configs.append(config)
        return self

    def remove_extra_spaces_def(self, r_e_s: bool = True) -> NormalizerConfiguration:
        """
        Helper function for adding configs
        """
        self.remove_extra_spaces = r_e_s
        return self

    def tokenizing(self, tokenization: bool = True) -> NormalizerConfiguration:
        """
        Helper function for adding configs
        """
        self.tokenization = tokenization
        return self
