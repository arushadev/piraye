# pylint: skip-file
from __future__ import annotations

from typing import Dict, Any


class CharModel:
    def __init__(self, char: str,
                 space_before: bool = None,
                 space_after: bool = None,
                 space_priority: int = None,
                 is_token: bool = None):
        self.space_after = space_after
        self.space_before = space_before
        self.char = char
        self.space_priority = space_priority
        self.is_token = is_token
        self.is_space = True if self.space_priority is not None else False

    @staticmethod
    def get_model_from_dict(data: Dict["str", Any], config: str) -> CharModel:
        return CharModel(data["map"][config]["char"],
                         data["clean"].get('space_before') if data.get("clean") else None,
                         data["clean"].get('space_after') if data.get("clean") else None,
                         data["clean"].get('space_priority') if data.get("clean") else None,
                         data["clean"].get('is_token') if data.get("clean") else None
                         )
