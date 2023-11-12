# pylint: skip-file
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(unsafe_hash=False, frozen=True)
class CharConfig:
    char: str
    space_before: bool = None
    space_after: bool = None
    space_priority: int = None
    is_token: bool = None

    @property
    def is_space(self) -> str:
        return self.space_priority is not None

    @staticmethod
    def from_dict(data: Dict, config: str) -> CharConfig:
        return CharConfig(data["map"][config]["char"],
                          data["clean"].get('space_before') if data.get("clean") else None,
                          data["clean"].get('space_after') if data.get("clean") else None,
                          data["clean"].get('space_priority') if data.get("clean") else None,
                          data["clean"].get('is_token') if data.get("clean") else None
                          )
