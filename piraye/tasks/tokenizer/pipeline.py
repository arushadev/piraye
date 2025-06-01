from typing import List
from .base_tokenizer import Tokenizer
from .token import Token

class TokenizerPipeline:
    """
    Pipeline for sequentially applying multiple tokenizers and merging their outputs.
    """

    def __init__(self, tokenizers: List[Tokenizer]):
        self.tokenizers = tokenizers

    def __call__(self, text: str) -> List[Token]:
        if not self.tokenizers:
            return []
        # Start with the first tokenizer's output
        tokens = self.tokenizers[0].tokenize(text)
        # Sequentially apply and merge each tokenizer
        for tokenizer in self.tokenizers[1:]:
            tokens = tokenizer.merge(text, tokens)
        return tokens
