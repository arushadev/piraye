"""Pipeline module for chaining multiple tokenizers."""
from typing import List
from .tokenizers.base_tokenizer import Tokenizer
from .token import Token


# pylint: disable=too-few-public-methods
class TokenizerPipeline(Tokenizer):
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
        Tokenizer.__init__(self)
        if tokenizers is None:
            raise ValueError("Tokenizers list cannot be None")
        self.tokenizers = tokenizers

    def tokenize(self, text: str) -> List[Token]:
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
            tokens = TokenizerPipeline.__merge(text, tokens, tokenizer.tokenize(text))

        return tokens

    @staticmethod
    # pylint: disable=too-many-branches,too-many-statements
    def __merge(text: str, previous_tokens: List[Token],
                new_tokens: List[Token]) -> List[Token]:
        """
        Merge new tokens with previously generated tokens.

        This method enables hierarchical tokenization by intelligently combining
        tokens from different tokenizers, handling overlapping and nested tokens.

        Args:
            text: The original input text
            previous_tokens: List of previously generated Token objects
            new_tokens: List of newly generated Token objects

        Returns:
            A list of merged Token objects
        """
        merged_tokens = []

        i, j = 0, 0
        current_token = None

        while i < len(previous_tokens) or j < len(new_tokens):
            default_pos = (len(text) + 1, len(text) + 1)
            prev = (previous_tokens[i] if i < len(previous_tokens)
                    else Token("", "", default_pos, []))
            new = (new_tokens[j] if j < len(new_tokens)
                   else Token("", "", default_pos, []))

            p_start, p_end = prev.position
            n_start, n_end = new.position

            if p_end <= n_start:
                if current_token:
                    current_token = TokenizerPipeline.__extend_token(
                        current_token, prev, text, prev)
                    merged_tokens.append(current_token)
                    current_token = None
                else:
                    merged_tokens.append(prev)
                i += 1

            elif n_end <= p_start:
                if current_token:
                    current_token = TokenizerPipeline.__extend_token(current_token, new, text)
                    merged_tokens.append(current_token)
                    current_token = None
                else:
                    merged_tokens.append(new)
                j += 1

            elif n_start <= p_start and p_end <= n_end:
                if current_token:
                    current_token = TokenizerPipeline.__extend_token(
                        current_token, prev, text, prev)
                else:
                    current_token = Token(new.content, new.type, new.position,
                                          new.sub_tokens + [prev])
                i += 1

            elif p_start <= n_start and n_end <= p_end:
                if current_token:
                    current_token = TokenizerPipeline.__extend_token(
                        current_token, new, text)
                else:
                    current_token = Token(prev.content, prev.type, prev.position,
                                          prev.sub_tokens + [new])
                j += 1

            elif p_start < n_start < p_end < n_end:
                if current_token:
                    current_token = TokenizerPipeline.__extend_token(
                        current_token, prev, text, prev)
                else:
                    current_token = prev
                i += 1

            elif n_start < p_start < n_end < p_end:
                if current_token:
                    current_token = TokenizerPipeline.__extend_token(
                        current_token, new, text)
                else:
                    current_token = new
                j += 1

            elif p_end == n_end:
                merged = Token(
                    content=text[min(p_start, n_start):p_end],
                    type=new.type,
                    position=(min(p_start, n_start), p_end),
                    sub_tokens=prev.sub_tokens + new.sub_tokens + [prev]
                )
                merged_tokens.append(merged)
                i += 1
                j += 1
                current_token = None

        return merged_tokens

    @staticmethod
    def __extend_token(current: Token, new: Token, text: str, child: Token | None = None) -> Token:
        """
        Extend a token by merging it with a new token.

        Args:
            current: The current token to extend
            new: The new token to merge with
            text: The original text
            child: Optional child token to add to sub_tokens

        Returns:
            A new extended Token object
        """
        return Token(
            content=text[current.position[0]:new.position[1]],
            type=current.type,
            position=(current.position[0], new.position[1]),
            sub_tokens=(current.sub_tokens + [child] if child
                        else current.sub_tokens)
        )
