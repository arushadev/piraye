import re
from typing import List

from .base_tokenizer import Tokenizer
from .token import Token


class RegexTokenizer(Tokenizer):
    """
    Tokenizer that uses regular expressions to tokenize text.
    """

    def __init__(self, pattern: str):
        """
        Initialize the RegexTokenizer with a given pattern.

        Args:
            pattern (str): The regex pattern to use for tokenization.
        """
        Tokenizer.__init__(self)
        self.pattern = pattern

    def tokenize(self, text: str):
        """
        Tokenize the input text using the regex pattern.

        Args:
            text (str): The input text to tokenize.

        Returns:
            list: A list of tokens.
        """
        text2 = self._clean_text(text)
        tokens: List[Token] = []
        for match in re.finditer(self.pattern, text2):
            token = Token(content=match.group(), position=(match.start(), match.end()), type=self.__class__.__name__,
                          sub_tokens=[])
            tokens.append(token)
        return tokens


class URLTokenizer(RegexTokenizer):
    """
    Tokenizer that uses regular expressions to tokenize URLs.
    """

    def __init__(self):
        """
        Initialize the URLTokenizer with a regex pattern for URLs.
        """
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        RegexTokenizer.__init__(self, pattern)

class EmailTokenizer(RegexTokenizer):
    """
    Tokenizer that uses regular expressions to tokenize email addresses.
    """

    def __init__(self):
        """
        Initialize the EmailTokenizer with a regex pattern for email addresses.
        """
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        RegexTokenizer.__init__(self, pattern)

