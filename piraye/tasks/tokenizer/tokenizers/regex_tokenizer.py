"""Regex-based tokenizer implementations."""
import re
from typing import List

from .base_tokenizer import Tokenizer
from ..token import Token


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


class URLTokenizer(RegexTokenizer):
    """
    Tokenizer for identifying and extracting URLs from text.
    
    This tokenizer uses a regex pattern to match HTTP and HTTPS URLs.
    """

    def __init__(self):
        """Initialize the URLTokenizer with a URL matching pattern."""
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        RegexTokenizer.__init__(self, pattern)

class EmailTokenizer(RegexTokenizer):
    """
    Tokenizer for identifying and extracting email addresses from text.
    
    This tokenizer uses a regex pattern to match standard email address formats.
    """

    def __init__(self):
        """Initialize the EmailTokenizer with an email matching pattern."""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        RegexTokenizer.__init__(self, pattern)

