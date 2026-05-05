"""Character-level text normalizer implementation."""
from __future__ import annotations

from typing import List, Tuple

from ..base_normalizer import Normalizer
from ..char_config import CharConfig
from ..mappings import MappingDict
from ..normalized_text import NormalizedText
from ...tokenizer.base_tokenizer import Tokenizer
from ...tokenizer.impl.nltk_tokenizer import NltkWordTokenizer


class NormalizationState:
    """
    Wrapper class to keep state of normalized text and compute shift
    """

    def __init__(self):
        self.__result = NormalizedText()
        self.__current_actual_position = 0
        self.__current_text_position = 0

    def add_char(self, char: str, original_pos: int | None, is_punctuation: bool = False):
        """
        Add a character and update tracking
        Args:
            char: char to be added to normalized text. can be zero length or length > 0
            original_pos: original pos of char in text if char is not exists in original text pass None
            is_punctuation: whether char is punctuation or not for tracking punctuation locations in normalized text
        Returns:
        """
        if original_pos is not None:
            current_shift = original_pos - self.__current_actual_position
            if current_shift != 0:
                self.__result.shifts.append((self.__current_text_position, current_shift))
            self.__current_actual_position = original_pos + len(char)
        else:
            self.__current_actual_position += len(char)
        self.__result.text += char
        if is_punctuation:
            self.__result.punc_positions.append(self.__current_text_position)
        self.__current_text_position += len(char)

    def finalize(self, text_length: int | None = None) -> NormalizedText:
        if text_length is not None:
            current_shift = text_length - self.__current_actual_position
            if current_shift != 0:
                self.__result.shifts.append((self.__current_text_position, current_shift))
        return self.__result

    def __str__(self):
        return f"Actual: {self.__current_actual_position}\t Text: {self.__current_text_position}"


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
        self.__configs = configs if configs is not None else []
        self.__remove_extra_spaces = remove_extra_spaces
        self.__mapping = MappingDict.load_jsons(self.__configs)

        if tokenization and tokenizer:
            self.__tokenizer = tokenizer
        elif tokenization:
            self.__tokenizer = NltkWordTokenizer()
        else:
            self.__tokenizer = None

    # pylint: disable=too-many-branches
    def normalize(self, text: str) -> tuple[str, NormalizedText]:
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
        is_token_list = self.__tokenize(text)
        state = NormalizationState()
        last = None

        for i, char in enumerate(text):
            is_token = is_token_list[i]
            mapping_char = self.__mapping.get(char)
            if not self.__remove_extra_spaces:
                if mapping_char and (not mapping_char.is_token or (mapping_char.is_token and is_token)):
                    char = mapping_char.char
                state.add_char(char, i, (mapping_char is not None) and mapping_char.is_punctuation)
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
                        state.add_char(last.char, None)
                    # If last char is not space and need space before current or after last
                    if last and last.is_space is not True and \
                            (current.space_before or last.space_after) and is_token:
                        state.add_char(" ", None)
                    if not current.is_token or (current.is_token and is_token):
                        state.add_char(current.char, i, current.is_punctuation)
                    else:
                        state.add_char(char, i, current.is_punctuation)
                    last = current
        if last and last.is_space:
            state.add_char(last.char, None)
        result = state.finalize(len(text))
        return result.text, result

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
        if not self.__tokenizer:
            return [True] * len(text)
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
