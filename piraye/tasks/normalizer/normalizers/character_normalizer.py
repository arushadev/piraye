"""Character-level text normalizer implementation."""
from __future__ import annotations

from typing import List, Tuple

from ..char_config import CharConfig
from ..mappings import MappingDict
from ...tokenizer.tokenizers.nltk_tokenizer import NltkWordTokenizer
from ...tokenizer.tokenizers.base_tokenizer import Tokenizer
from .base_normalizer import Normalizer
from ..normalization_result import NormalizationResult


# pylint: disable=too-few-public-methods
class CharacterNormalizer(Normalizer):
    """
    Character-level normalizer implementation.
    
    This normalizer processes text character by character, applying configured
    transformations such as alphabet normalization, digit conversion, and
    punctuation standardization.
    
    Attributes:
        __configs: List of normalization configuration names
        __remove_extra_spaces: Whether to consolidate multiple spaces
        __tokenizer: Optional tokenizer for token-aware normalization
    """

    def __init__(self, configs: List[str] | None = None, remove_extra_spaces: bool = True,
                 tokenization: bool = True, tokenizer: Tokenizer | None = None):
        """
        Initialize the CharacterNormalizer.
        
        Args:
            configs: List of normalizer configuration names to apply
            remove_extra_spaces: Whether to remove extra spaces during normalization
            tokenization: Whether to use tokenization during normalization
            tokenizer: Custom tokenizer (defaults to NltkWordTokenizer if tokenization is True)
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
                self.__tokenizer = NltkWordTokenizer()
        else:
            self.__tokenizer = None

    # pylint: disable=too-many-branches
    def normalize(self, text: str) -> tuple[str, NormalizationResult]:
        """
        Normalize the given text according to configured rules.
        
        This method processes text character by character, applying normalization
        rules while tracking position shifts for mapping back to the original text.
        
        Args:
            text: Text to be normalized
            
        Returns:
            A tuple containing:
                - Normalized text
                - NormalizationResult with shifts and punctuation locations
        """
        if self.__tokenizer:
            is_token_list = self.__tokenize(text)
        else:
            is_token_list = [True] * len(text)
        result: str = ""
        last = None
        current_shift = 0
        last_added_shift = 0
        shifts: list[tuple[int, int]] = []
        punc_positions: list[int] = []

        for i, char in enumerate(text):
            is_token = is_token_list[i]
            mapping_char = self.__mapping.get(char)
            if not self.__remove_extra_spaces:
                if mapping_char and \
                        (not mapping_char.is_token or (mapping_char.is_token and is_token)):
                    char = mapping_char.char
                result += char
                current_shift = i - len(result) + 1
                # Track punctuation locations in normalized text
                if mapping_char and mapping_char.is_punctuation:
                    punc_positions.append(len(result) - 1)
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
                    # Track punctuation locations in normalized text
                    if current.is_punctuation:
                        punc_positions.append(len(result) - 1)
                    current_shift = i - len(result) + 1
                    last = current
            if current_shift != last_added_shift:
                shifts.append((len(result) - 1, current_shift))
                last_added_shift = current_shift
        if last and last.is_space:
            result += last.char
            if current_shift != last_added_shift:
                shifts.append((len(result) - 1, current_shift))
        return result, NormalizationResult(shifts=shifts, punc_positions=punc_positions)

    def __tokenize(self, text: str) -> List[bool]:
        """
        Create a boolean list indicating which characters are tokens.
        
        This method uses the configured tokenizer to identify token boundaries
        and returns a boolean list where True indicates the character is part of a token.
        
        Args:
            text: The input text to analyze
            
        Returns:
            List of booleans, one per character, indicating token membership
        """
        is_token_list = [False] * len(text)
        spans = self.__tokenizer.tokenize(text)
        for span in spans:
            start = span.position[0]
            end = span.position[1]
            if start + 1 == end:
                is_token_list[start] = True
        return is_token_list

    def span_normalize(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Normalize text and return spans of normalized tokens.

        Args:
            text: The input text to normalize

        Returns:
            List of tuples containing (start, end, normalized_text)
        """
        raise NotImplementedError()
