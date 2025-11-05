"""Base regex tokenizer class."""
import re
from typing import List

from ..base_tokenizer import Tokenizer
from ...token import Token


# pylint: disable=too-few-public-methods
class RegexTokenizer(Tokenizer):
    """
    Tokenizer that uses regular expressions to identify tokens.

    This class provides a flexible base for creating tokenizers that use
    regex patterns to match specific types of content in text.
    """

    def __init__(self, pattern: str):
        """
        Initialize the RegexTokenizer with a regex pattern.

        Args:
            pattern: The regex pattern to use for tokenization
        """
        Tokenizer.__init__(self)
        self.pattern = pattern
        self._compiled_pattern = re.compile(pattern)

    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize the input text using the regex pattern.

        Args:
            text: The input text to tokenize

        Returns:
            List of Token objects matching the pattern
        """
        text2 = self._clean_text(text)
        tokens: List[Token] = []

        for match in self._compiled_pattern.finditer(text2):
            token = Token(
                content=match.group(),
                position=(match.start(), match.end()),
                type=self.__class__.__name__,
                sub_tokens=[]
            )
            tokens.append(token)

        return tokens
