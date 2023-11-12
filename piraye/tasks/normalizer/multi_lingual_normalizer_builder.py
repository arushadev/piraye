"""This module is for config set """
from __future__ import annotations

from .character_normalizer import Normalizer
from .multi_lingual_normalizer import MultiLingualNormalizer, TokenizationLevel
from ...tokenizer import Tokenizer


class MultiLingualNormalizerBuilder:
    """
    A builder class for multilingual normalizer
    ...

    Attributes
    ----------
    __configs : List[str] or List[Config]
        list of desired configs

    Methods
    -------
    build():
        build an instance of normalizer with current config
    """

    def __init__(self, configs=None):
        """
        constructor
        :param configs default normalizers for each language
        """
        self.__tokenizer = None
        if configs is None:
            configs = {}
        self.__configs = configs
        self.__tokenization_level = TokenizationLevel.SENTENCE_LEVEL
        self.__main_normalizer_lang = 'fa'

    def build(self) -> MultiLingualNormalizer:
        """
        build function of multilingual normalizer
        """
        return MultiLingualNormalizer(self.__configs, self.__main_normalizer_lang,
                                      self.__tokenization_level, self.__tokenizer)

    def tokenization_level(self, tokenization_level: TokenizationLevel) -> MultiLingualNormalizerBuilder:
        """
        Helper function for tokenization level
        """
        self.__tokenization_level = tokenization_level
        return self

    def word_level(self) -> MultiLingualNormalizerBuilder:
        """
        Helper function for tokenization level
        """
        self.__tokenization_level = TokenizationLevel.WORD_LEVEL
        return self

    def sentence_level(self) -> MultiLingualNormalizerBuilder:
        """
        Helper function for tokenization level
        """
        self.__tokenization_level = TokenizationLevel.SENTENCE_LEVEL
        return self

    def lingua_mode(self) -> MultiLingualNormalizerBuilder:
        """
        Helper function for tokenization level
        """
        self.__tokenization_level = TokenizationLevel.LINGUA_MIXED_MODE
        return self

    def main_normalizer_lang(self, main_normalizer_lang: str) -> MultiLingualNormalizerBuilder:
        """
        Helper function for main normalizer language
        """
        self.__main_normalizer_lang = main_normalizer_lang
        return self

    def set_normalizer(self, lang: str, normalizer: Normalizer) -> MultiLingualNormalizerBuilder:
        """
        Set a normalizer for a language
        """
        self.__configs[lang] = normalizer
        return self

    def set_tokenizer(self, tokenizer: Tokenizer) -> MultiLingualNormalizerBuilder:
        """
        Helper function for tokenizer
        """
        self.__tokenizer = tokenizer
        return self
