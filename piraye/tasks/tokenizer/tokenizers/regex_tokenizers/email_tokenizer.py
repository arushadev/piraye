"""Email tokenizer implementation."""
from .base_regex_tokenizer import RegexTokenizer


# pylint: disable=too-few-public-methods
class EmailTokenizer(RegexTokenizer):
    """
    Tokenizer for identifying and extracting email addresses from text.

    This tokenizer uses a regex pattern to match standard email address formats.
    """

    def __init__(self):
        """Initialize the EmailTokenizer with an email matching pattern."""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        RegexTokenizer.__init__(self, pattern)
