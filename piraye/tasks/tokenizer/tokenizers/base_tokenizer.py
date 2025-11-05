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

    def __call__(self, text: str) -> List[Token]:
        return self.tokenize(text)

    @abstractmethod
    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize the input text into a list of tokens.
        
        Args:
            text: The input string to be tokenized
            
        Returns:
            A list of Token objects extracted from the input text
        """
