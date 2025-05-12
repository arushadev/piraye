"""Base class of tokenizer"""
from abc import ABC, abstractmethod
from typing import List

from .token import Token


class Tokenizer(ABC):
    """
    Abstract class for tokenizing
    """

    def __init__(self):
        pass

    @abstractmethod
    def tokenize(self, text: str) -> List[Token]:
        pass

    def merge(self, text: str, previous_tokens: List[Token]) -> List[Token]:
        """
        Merge tokens
        """
        new_tokens = self.tokenize(text)
        new_token_index = 0
        previous_token_index = 0
        current_token: Token | None = None
        merged_tokens = []
        while True:
            previous_token = previous_tokens[previous_token_index]
            new_token = new_tokens[new_token_index]
            if previous_token.position[0] < previous_token.position[1] < new_token.position[0] < new_token.position[1]:
                # Previous_Token before new token
                if current_token:
                    current_token = Token(content=text[current_token.position[0]:previous_token.position[1]],
                                          position=(current_token.position[0], previous_token.position[1]),
                                          type=current_token.type,
                                          sub_tokens=[*current_token.sub_tokens, previous_token])
                    merged_tokens.append(current_token)
                    previous_token_index += 1
                    current_token = None
                else:
                    merged_tokens.append(previous_token)
                    previous_token_index += 1  # Done
            elif previous_token.position[0] < new_token.position[0] < previous_token.position[1] < new_token.position[
                1]:
                # Previous_Token overlapped before new token
                if current_token:
                    current_token = Token(content=current_token.content,
                                          position=current_token.position,
                                          type=current_token.type,
                                          sub_tokens=[*current_token.sub_tokens, previous_token])
                    previous_token_index += 1
                else:
                    current_token = previous_token
                    previous_token_index += 1
                pass
            elif new_token.position[0] < previous_token.position[0] < previous_token.position[1] < new_token.position[
                1]:
                # Previous_Token is child of new token
                if current_token:
                    current_token = Token(content=current_token.content,
                                          position=current_token.position,
                                          type=current_token.type,
                                          sub_tokens=[*current_token.sub_tokens, previous_token])
                    previous_token_index += 1
                else:
                    current_token = new_token
                    previous_token_index += 1
                pass

        return merged_tokens
