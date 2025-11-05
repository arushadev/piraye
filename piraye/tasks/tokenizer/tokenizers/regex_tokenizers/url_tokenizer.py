"""URL tokenizer implementation."""
from .base_regex_tokenizer import RegexTokenizer


# pylint: disable=too-few-public-methods
class URLTokenizer(RegexTokenizer):
    """
    Tokenizer for identifying and extracting URLs from text.

    This tokenizer uses a regex pattern to match HTTP and HTTPS URLs.
    """

    def __init__(self):
        """Initialize the URLTokenizer with a URL matching pattern."""
        pattern = (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                   r'[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        RegexTokenizer.__init__(self, pattern)
