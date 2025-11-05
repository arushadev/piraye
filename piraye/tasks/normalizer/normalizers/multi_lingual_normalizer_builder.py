"""Builder for multi-lingual normalizer configuration."""
from __future__ import annotations

from typing import Dict

from .character_normalizer import Normalizer
from .multi_lingual_normalizer import MultiLingualNormalizer, TokenizationLevel
from ...tokenizer.tokenizers.base_tokenizer import Tokenizer


class MultiLingualNormalizerBuilder:
    """
    Builder class for creating MultiLingualNormalizer instances.

    This builder provides a fluent interface for configuring multi-lingual
    text normalization with custom normalizers for each language and
    different tokenization strategies.

    Example:
        >>> builder = MultiLingualNormalizerBuilder()
        >>> normalizer = (builder
        ...     .word_level()
        ...     .main_normalizer_lang('fa')
        ...     .build())
    """

    def __init__(self, configs: Dict[str, Normalizer] | None = None):
        """
        Initialize the MultiLingualNormalizerBuilder.

        Args:
            configs: Dictionary of language codes to normalizers.
                    If None, default normalizers will be used.
        """
        self.__tokenizer: Tokenizer | None = None
        self.__configs = configs if configs is not None else {}
        self.__tokenization_level = TokenizationLevel.SENTENCE_LEVEL
        self.__main_normalizer_lang = 'fa'

    def build(self) -> MultiLingualNormalizer:
        """
        Build and return a MultiLingualNormalizer instance.

        Returns:
            Configured MultiLingualNormalizer instance
        """
        return MultiLingualNormalizer(
            self.__configs,
            self.__main_normalizer_lang,
            self.__tokenization_level,
            self.__tokenizer
        )

    def tokenization_level(
            self,
            tokenization_level: TokenizationLevel
    ) -> MultiLingualNormalizerBuilder:
        """
        Set the tokenization level for language detection.

        Args:
            tokenization_level: The tokenization level to use

        Returns:
            Self for method chaining
        """
        self.__tokenization_level = tokenization_level
        return self

    def word_level(self) -> MultiLingualNormalizerBuilder:
        """
        Set tokenization to word level.

        Returns:
            Self for method chaining
        """
        self.__tokenization_level = TokenizationLevel.WORD_LEVEL
        return self

    def sentence_level(self) -> MultiLingualNormalizerBuilder:
        """
        Set tokenization to sentence level.

        Returns:
            Self for method chaining
        """
        self.__tokenization_level = TokenizationLevel.SENTENCE_LEVEL
        return self

    def lingua_mode(self) -> MultiLingualNormalizerBuilder:
        """
        Set tokenization to Lingua library mixed mode.

        Returns:
            Self for method chaining
        """
        self.__tokenization_level = TokenizationLevel.LINGUA_MIXED_MODE
        return self

    def main_normalizer_lang(self, main_normalizer_lang: str) -> MultiLingualNormalizerBuilder:
        """
        Set the main normalizer language.

        Args:
            main_normalizer_lang: Language code ('fa', 'ar', or 'en')

        Returns:
            Self for method chaining
        """
        self.__main_normalizer_lang = main_normalizer_lang
        return self

    def set_normalizer(self, lang: str, normalizer: Normalizer) -> MultiLingualNormalizerBuilder:
        """
        Set a custom normalizer for a specific language.

        Args:
            lang: Language code
            normalizer: Normalizer instance for the language

        Returns:
            Self for method chaining
        """
        self.__configs[lang] = normalizer
        return self

    def set_tokenizer(self, tokenizer: Tokenizer) -> MultiLingualNormalizerBuilder:
        """
        Set a custom tokenizer.

        Args:
            tokenizer: Custom tokenizer instance

        Returns:
            Self for method chaining
        """
        self.__tokenizer = tokenizer
        return self
