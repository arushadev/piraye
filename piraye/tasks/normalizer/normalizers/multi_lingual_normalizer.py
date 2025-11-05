"""Multi-lingual text normalizer implementation."""
from enum import Enum
from typing import Dict

# pylint: disable=import-error,no-name-in-module
from lingua import Language, LanguageDetectorBuilder

from ..normalizer_builder import NormalizerBuilder
from ...tokenizer.tokenizers.nltk_tokenizer import (
    Tokenizer, NltkWordTokenizer, NltkSentenceTokenizer
)
from .base_normalizer import Normalizer
from ..normalization_result import NormalizationResult


class TokenizationLevel(Enum):
    """
    Enumeration of tokenization levels for language detection.

    Attributes:
        WORD_LEVEL: Detect language at the word level
        SENTENCE_LEVEL: Detect language at the sentence level
        LINGUA_MIXED_MODE: Use Lingua library's mixed-mode detection
    """
    WORD_LEVEL = 1
    SENTENCE_LEVEL = 2
    LINGUA_MIXED_MODE = 3


# pylint: disable=too-few-public-methods
class MultiLingualNormalizer(Normalizer):
    """
    Normalizer that handles multiple languages in the same text.

    This normalizer tokenizes text and detects the language of each token,
    then applies the appropriate language-specific normalizer. It supports
    Persian (Farsi), Arabic, and English languages.

    The normalizer can work at different tokenization levels:
    - Word level: Each word is detected and normalized separately
    - Sentence level: Each sentence is detected and normalized separately
    - Lingua mixed mode: Uses Lingua library's advanced language detection
    """

    def __init__(self,
                 configs: Dict[str, Normalizer] | None = None,
                 main_normalizer_lang: str = 'fa',
                 tokenization_level: TokenizationLevel = TokenizationLevel.WORD_LEVEL,
                 tokenizer: Tokenizer | None = None):
        """
        Initialize the MultiLingualNormalizer.

        Args:
            configs: Dictionary mapping language codes to their normalizers.
                    Defaults to Persian, Arabic, and English normalizers.
            main_normalizer_lang: Main language code for normalizing non-detected text
            tokenization_level: Level at which to perform language detection
            tokenizer: Custom tokenizer to use (optional)
        """
        # Set default normalizers if none provided
        if configs is None:
            configs = {
                'fa': (NormalizerBuilder()
                       .alphabet_fa().alphabet_en().digit_fa().punctuation_fa()
                       .diacritic_delete().space_normal().tokenizing()
                       .remove_extra_spaces().build()),
                'ar': (NormalizerBuilder()
                       .alphabet_ar().alphabet_en().digit_ar().punctuation_ar()
                       .diacritic_delete().space_normal().tokenizing()
                       .remove_extra_spaces().build()),
                'en': (NormalizerBuilder()
                       .alphabet_en().digit_en().punctuation_en()
                       .diacritic_delete().space_normal().tokenizing()
                       .remove_extra_spaces().build()),
            }

        self.__configs = configs
        self.__tokenization_level = tokenization_level
        self.__main_normalizer_lang = main_normalizer_lang

        # Set up tokenizers
        if tokenizer is not None:
            # Custom tokenizer provided (reserved for future use)
            pass

        self.__word_tokenizer = NltkWordTokenizer()
        self.__sentence_tokenizer = NltkSentenceTokenizer()

        # Initialize language detector
        languages = [Language.PERSIAN, Language.ARABIC, Language.ENGLISH]
        self.__detector = LanguageDetectorBuilder.from_languages(*languages).build()

    def normalize(self, text: str) -> tuple[str, NormalizationResult]:
        """
        Normalize text with multi-language support.

        Args:
            text: The input text to normalize

        Returns:
            A tuple containing:
                - Normalized text
                - NormalizationResult with shifts and punctuation locations
        """
        result = ''
        main_normalizer = self.__configs[self.__main_normalizer_lang]

        if self.__tokenization_level is TokenizationLevel.LINGUA_MIXED_MODE:
            result = self._normalize_lingua_mode(text, main_normalizer)
        else:
            result = self._normalize_token_mode(text, main_normalizer)

        return result, NormalizationResult()

    def _normalize_lingua_mode(self, text: str, main_normalizer: Normalizer) -> str:
        """
        Normalize text using Lingua library's mixed-mode detection.

        Args:
            text: Input text
            main_normalizer: Normalizer for undetected sections

        Returns:
            Normalized text
        """
        result = ''
        lingua = self.__detector.detect_multiple_languages_of(text)
        i = 0

        for det_res in lingua:
            # Normalize text before detected segment
            if det_res.start_index > i:
                result += main_normalizer.normalize(text[i:det_res.start_index])[0]

            # Normalize detected segment
            normalized = self.__normalize_sub_text(
                text[det_res.start_index:det_res.end_index],
                det_res.language
            )
            result += normalized[0]
            i = det_res.end_index

        # Normalize remaining text
        if i < len(text):
            result += main_normalizer.normalize(text[i:])[0]

        return result

    def _normalize_token_mode(self, text: str, main_normalizer: Normalizer) -> str:
        """
        Normalize text using word or sentence level tokenization.

        Args:
            text: Input text
            main_normalizer: Normalizer for non-token sections

        Returns:
            Normalized text
        """
        result = ''

        # Select appropriate tokenizer
        if self.__tokenization_level is TokenizationLevel.WORD_LEVEL:
            spans = self.__word_tokenizer.tokenize(text)
        else:
            spans = self.__sentence_tokenizer.tokenize(text)

        i = 0
        for span in spans:
            start, end = span.position

            # Normalize text before token
            if start > i:
                result += main_normalizer.normalize(text[i:start])[0]

            # Normalize token
            normalized = self.__normalize_sub_text(span.content)
            result += normalized[0]
            i = end

        # Normalize remaining text
        if i < len(text):
            result += main_normalizer.normalize(text[i:])[0]

        return result

    def __normalize_sub_text(
            self, sub_text: str,
            lang: Language | None = None
    ) -> tuple[str, NormalizationResult]:
        """
        Normalize a substring with detected or provided language.

        Args:
            sub_text: Text to normalize
            lang: Detected language (if None, will be detected)

        Returns:
            A tuple containing normalized text and NormalizationResult
        """
        language = (lang if lang is not None
                    else self.__detector.detect_language_of(sub_text))
        normalizer: Normalizer = self.__configs[self.__main_normalizer_lang]

        match language:
            case Language.ARABIC:
                normalizer = self.__configs['ar']
            case Language.PERSIAN:
                normalizer = self.__configs['fa']
            case Language.ENGLISH:
                normalizer = self.__configs['en']

        return normalizer.normalize(sub_text)
