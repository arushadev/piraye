from typing import List, Self

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    content: str
    type: str
    position: tuple[int, int]
    sub_tokens: List[Self]
