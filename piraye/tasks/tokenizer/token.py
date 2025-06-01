from typing import List, Self

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    content: str
    type: str
    position: tuple[int, int]
    sub_tokens: List[Self]

    def __str__(self):
        return f"Token(type={self.type}, content={self.content!r}, position={self.position}, sub_tokens={len(self.sub_tokens)})"
