"""Base class of tokenizer"""
from abc import ABC, abstractmethod
from typing import List

from .token import Token
from ..normalizer.mappings import MappingDict


class Tokenizer(ABC):
    """
    An abstract base class that defines the interface for text tokenization.
    Subclasses should implement methods for splitting input text into tokens,
    enabling flexible and extensible tokenization strategies for various use cases.
    """

    def __init__(self):
        self._en_mapping = MappingDict.load_jsons(["digit_en", "punc_en"])
        self._space_mapping = MappingDict.load_jsons(["space_keep"])

    def _clean_text(self, text: str) -> str:
        """
        Clean the input text by replacing digits and punctuation with normalized versions.
        """
        return ''.join([char if not self._en_mapping.get(char)
                        else self._en_mapping.get(char).char for char in text])

    @abstractmethod
    def tokenize(self, text: str) -> List[Token]:
        """
        Parameters
        ----------
        text : str
            The input string to be tokenized.

        Returns
        -------
        List[Token]
            A list of Token objects extracted from the input text.
        """
        pass

    def merge(self, text: str, previous_tokens: List[Token]) -> List[Token]:
        """
        Parameters
        ----------
        text : str
            The input string to be tokenized and merged.
        previous_tokens : List[Token]
            The list of previously generated Token objects.

        Returns
        -------
        List[Token]
            A list of merged Token objects.
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
                    current_token = self._extend_token(current_token, prev, text)
                    merged_tokens.append(current_token)
                    current_token = None
                else:
                    merged_tokens.append(prev)
                i += 1

            elif n_end <= p_start:
                if current_token:
                    current_token = self._extend_token(current_token, new, text)
                    merged_tokens.append(current_token)
                    current_token = None
                else:
                    merged_tokens.append(new)
                j += 1

            elif p_start <= n_start and n_end <= p_end:
                if current_token:
                    current_token = self._extend_token(current_token, new, text)
                else:
                    current_token = Token(prev.content, prev.type, prev.position, prev.sub_tokens + [new])
                j += 1

            elif n_start <= p_start and p_end <= n_end:
                if current_token:
                    current_token = self._extend_token(current_token, prev, text)
                else:
                    current_token = Token(new.content, new.type, new.position, new.sub_tokens + [prev])
                i += 1

            elif p_start < n_start < p_end < n_end:
                if current_token:
                    current_token = self._extend_token(current_token, prev, text)
                else:
                    current_token = prev
                i += 1

            elif n_start < p_start < n_end < p_end:
                if current_token:
                    current_token = self._extend_token(current_token, new, text)
                else:
                    current_token = new
                j += 1

            elif p_end == n_end:
                merged = Token(
                    content=text[min(p_start, n_start):p_end],
                    type=new.type,
                    position=(min(p_start, n_start), p_end),
                    sub_tokens=prev.sub_tokens + new.sub_tokens + [prev, new]
                )
                merged_tokens.append(merged)
                i += 1
                j += 1
                current_token = None

        return merged_tokens

    def _extend_token(self, current: Token, new: Token, text: str) -> Token:
        return Token(
            content=text[current.position[0]:new.position[1]],
            type=current.type,
            position=(current.position[0], new.position[1]),
            sub_tokens=current.sub_tokens + [new]
        )
