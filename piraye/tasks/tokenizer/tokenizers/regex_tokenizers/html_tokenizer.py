"""HTML tokenizer implementation."""
from .base_regex_tokenizer import RegexTokenizer


# pylint: disable=too-few-public-methods
class HTMLTokenizer(RegexTokenizer):
    """
    Tokenizer for identifying and extracting HTML tags from text.

    This tokenizer uses a regex pattern to match HTML opening tags, closing tags,
    self-closing tags, and comments.
    """

    def __init__(self):
        """Initialize the HTMLTokenizer with an HTML tag matching pattern."""
        pattern = r'<(?:!--.*?--|[^>]+)>'
        RegexTokenizer.__init__(self, pattern)
