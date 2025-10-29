from typing import List
from .tokenizers.base_tokenizer import Tokenizer
from .token import Token


class TokenizerPipeline:
    """
    Pipeline for sequentially applying multiple tokenizers and merging their outputs.

    This class enables hierarchical tokenization by chaining multiple tokenizers.
    Each tokenizer in the pipeline processes and refines the output of the previous one.

    Example:
        >>> pipeline = TokenizerPipeline([
        ...     SpacySentenceTokenizer(),
        ...     URLTokenizer()
        ... ])
        >>> tokens = pipeline("Visit https://example.com for more info.")
    """

    def __init__(self, tokenizers: List[Tokenizer]):
        """
        Initialize the TokenizerPipeline.

        Args:
            tokenizers: List of tokenizers to apply sequentially

        Raises:
            ValueError: If tokenizers list is None
        """
        if tokenizers is None:
            raise ValueError("Tokenizers list cannot be None")
        self.tokenizers = tokenizers

    def __call__(self, text: str) -> List[Token]:
        """
        Apply the tokenizer pipeline to the input text.

        Args:
            text: Input text to tokenize

        Returns:
            List of Token objects representing the tokenized and merged text
        """
        if not self.tokenizers:
            return []

        if not text:
            return []

        # Start with the first tokenizer's output
        tokens = self.tokenizers[0].tokenize(text)

        # Sequentially apply and merge each tokenizer
        for tokenizer in self.tokenizers[1:]:
            tokens = tokenizer.merge(text, tokens)

        return tokens
