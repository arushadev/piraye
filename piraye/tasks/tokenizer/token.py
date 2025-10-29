"""Token data structure for representing tokenized text elements."""
from typing import List, Self
from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    """
    Represents a token with its content, type, position, and sub-tokens.

    Attributes:
        content: The text content of the token
        type: The type or name of the tokenizer that created this token
        position: Start and end indices (start, end) of the token in the original text
        sub_tokens: List of child tokens if this token is composed of smaller tokens

    Example:
        >>> token = Token(content="Hello", type="Word", position=(0, 5), sub_tokens=[])
        >>> print(token)
        Token(type=Word, content='Hello', position=(0, 5), sub_tokens=0)
    """
    content: str
    type: str
    position: tuple[int, int]
    sub_tokens: List[Self]

    def __str__(self) -> str:
        """Return a string representation of the token."""
        return (f"Token(type={self.type}, content={self.content!r}, "
                f"position={self.position}, sub_tokens={len(self.sub_tokens)})")
