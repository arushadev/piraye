"""Base class for all tokenizers."""
from abc import ABC, abstractmethod
from typing import List

from ..token import Token
from ...normalizer.mappings import MappingDict


class Tokenizer(ABC):
    """
    Abstract base class that defines the interface for text tokenization.
    
    Subclasses should implement the tokenize method to split input text into tokens,
    enabling flexible and extensible tokenization strategies for various use cases.
    
    The class also provides a merge method for hierarchical tokenization, allowing
    different tokenizers to be combined in a pipeline.
    """

    def __init__(self):
        """Initialize the tokenizer with English mappings for normalization."""
        self._en_mapping = MappingDict.load_jsons(["digit_en", "punc_en"])
        self._space_mapping = MappingDict.load_jsons(["space_keep"])

    def _clean_text(self, text: str) -> str:
        """
        Clean the input text by normalizing digits and punctuation.
        
        Args:
            text: The input text to clean
            
        Returns:
            Cleaned text with normalized characters
        """
        return ''.join([
            self._en_mapping.get(char).char if self._en_mapping.get(char) else char
            for char in text
        ])

    @abstractmethod
    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize the input text into a list of tokens.
        
        Args:
            text: The input string to be tokenized
            
        Returns:
            A list of Token objects extracted from the input text
        """
        pass

    def merge(self, text: str, previous_tokens: List[Token]) -> List[Token]:
        """
        Merge new tokens with previously generated tokens.
        
        This method enables hierarchical tokenization by intelligently combining
        tokens from different tokenizers, handling overlapping and nested tokens.
        
        Args:
            text: The original input text
            previous_tokens: List of previously generated Token objects
            
        Returns:
            A list of merged Token objects
        """
        new_tokens = self.tokenize(text)
        merged_tokens = []

        i, j = 0, 0
        current_token = None

        while i < len(previous_tokens) or j < len(new_tokens):
            prev = previous_tokens[i] if i < len(previous_tokens) else Token("", "", (len(text) + 1, len(text) + 1), [])
            new = new_tokens[j] if j < len(new_tokens) else Token("", "", (len(text) + 1, len(text) + 1), [])

            p_start, p_end = prev.position
            n_start, n_end = new.position

            if p_end <= n_start:
                if current_token:
                    current_token = Tokenizer._extend_token(current_token, prev, text, prev)
                    merged_tokens.append(current_token)
                    current_token = None
                else:
                    merged_tokens.append(prev)
                i += 1

            elif n_end <= p_start:
                if current_token:
                    current_token = Tokenizer._extend_token(current_token, new, text)
                    merged_tokens.append(current_token)
                    current_token = None
                else:
                    merged_tokens.append(new)
                j += 1

            elif n_start <= p_start and p_end <= n_end:
                if current_token:
                    current_token = Tokenizer._extend_token(current_token, prev, text, prev)
                else:
                    current_token = Token(new.content, new.type, new.position, new.sub_tokens + [prev])
                i += 1

            elif p_start <= n_start and n_end <= p_end:
                if current_token:
                    current_token = Tokenizer._extend_token(current_token, new, text)
                else:
                    current_token = Token(prev.content, prev.type, prev.position, prev.sub_tokens + [new])
                j += 1



            elif p_start < n_start < p_end < n_end:
                if current_token:
                    current_token = Tokenizer._extend_token(current_token, prev, text, prev)
                else:
                    current_token = prev
                i += 1

            elif n_start < p_start < n_end < p_end:
                if current_token:
                    current_token = Tokenizer._extend_token(current_token, new, text)
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
    def _extend_token(current: Token, new: Token, text: str, child: Token | None = None) -> Token:
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
            sub_tokens=current.sub_tokens + [child] if child else current.sub_tokens
        )
