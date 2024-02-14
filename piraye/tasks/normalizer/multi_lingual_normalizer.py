"""This module includes MultiLingualNormalizer class for normalizing texts"""
from abc import ABC
from enum import Enum
from typing import List, Tuple

from lingua import Language, LanguageDetectorBuilder

from .normalizer_builder import NormalizerBuilder
from ..tokenizer.nltk_tokenizer import NltkTokenizer, Tokenizer
from ...normalizer import Normalizer


class TokenizationLevel(Enum):
    """
    Level of text for language detection
    """
    WORD_LEVEL = 1
    SENTENCE_LEVEL = 2
    LINGUA_MIXED_MODE = 3


# pylint: disable=too-few-public-methods
class MultiLingualNormalizer(Normalizer, ABC):
    """
    Normalize the input text handling multiple languages.

    Tokenizes the text into words or sentences based on
    self.__tokenization_level. Detects the language of each
    token and normalizes using the appropriate Normalizer.
    """

    def __init__(self, configs: dict[str, Normalizer] = None,
                 main_normalizer_lang: str = 'fa',
                 tokenization_level: TokenizationLevel = TokenizationLevel.WORD_LEVEL,
                 tokenizer: Tokenizer = None):
        """ff
        constructor
        :param  configs : List[str]
            list of desired configs
        :param  main_normalizer_lang : str
            that determines main normalization language (for space characters)
        :param  tokenization_level: TokenizationLevel
            tokenization level: word-level, sentence-level and lingua libaray mode
        :param  tokenizer: Tokenizer
            default tokenizer
        """
        # Create a blank Tokenizer with just the English vocab
        if configs is None:
            configs = {
                'fa': NormalizerBuilder().alphabet_fa().alphabet_en().digit_fa().punctuation_fa().diacritic_delete()
                .space_normal().tokenizing().remove_extra_spaces().build(),
                'ar': NormalizerBuilder().alphabet_ar().alphabet_en().digit_ar().punctuation_ar().diacritic_delete()
                .space_normal().tokenizing().remove_extra_spaces().build(),
                'en': NormalizerBuilder().alphabet_en().digit_en().punctuation_en().diacritic_delete()
                .space_normal().tokenizing().remove_extra_spaces().build(),
            }
        self.__configs = configs
        self.__tokenization_level = tokenization_level
        self.__main_normalizer_lang = main_normalizer_lang
        if tokenizer:
            self.__tokenizer = tokenizer
        else:
            self.__tokenizer = NltkTokenizer()

        languages = [Language.PERSIAN, Language.ARABIC, Language.ENGLISH]
        self.__detector = LanguageDetectorBuilder.from_languages(*languages).build()

    def normalize(self, text: str) -> str:
        """
        returns a normalized text
        :param text: the input text, paragraphs are not retained.
        :return: normalized text
        """
        result = ''
        main_normalizer = self.__configs[self.__main_normalizer_lang]
        if self.__tokenization_level is TokenizationLevel.LINGUA_MIXED_MODE:
            lingua = self.__detector.detect_multiple_languages_of(text)
            i = 0
            for det_res in lingua:
                if det_res.start_index > i:
                    result += main_normalizer.normalize(text[i: det_res.start_index])
                normalized = self.__normalize_sub_text(text[det_res.start_index: det_res.end_index], det_res.language)
                result += normalized
                i = det_res.end_index
            if i < len(text):
                result += main_normalizer.normalize(text[i:])
        else:
            spans: List[Tuple[int, int, str]]
            if self.__tokenization_level is TokenizationLevel.WORD_LEVEL:
                spans = self.__tokenizer.word_span_tokenize(text)
            else:
                spans = self.__tokenizer.sentence_span_tokenize(text)
            i = 0
            for (start, end, word) in spans:
                if start > i:
                    result += main_normalizer.normalize(text[i: start])
                normalized = self.__normalize_sub_text(word)
                result += normalized
                i = end
            if i < len(text):
                result += main_normalizer.normalize(text[i:])
        return result

    def __normalize_sub_text(self, sub_text: str, lang: Language | None = None) -> str:
        """
        Normalize text
        :param sub_text:
        :param lang:
        :return:
        """
        language = lang if lang is not None else self.__detector.detect_language_of(sub_text)
        normalizer: Normalizer = self.__configs[self.__main_normalizer_lang]
        match language:
            case Language.ARABIC:
                normalizer = self.__configs['ar']
            case Language.PERSIAN:
                normalizer = self.__configs['fa']
            case Language.ENGLISH:
                normalizer = self.__configs['en']
        return normalizer.normalize(sub_text)

    def span_normalize(self, text: str) -> List[Tuple[int, int, str]]:
        raise NotImplementedError()
