from typing import List

from .base_tokenizer import Tokenizer
from .token import Token


class ParagraphTokenizer(Tokenizer):
    def __init__(self):
        Tokenizer.__init__(self)

    def tokenize(self, text: str) -> List[Token]:
        start = 0
        end = 0
        paragraphs: List[Token] = []
        for i, char in enumerate(text):
            if char == "\n":
                if end > start:
                    paragraphs.append(
                        Token(content=text[start:end], position=(start, end), type="Paragraph", sub_tokens=[]))
                    start = end
            elif self._space_mapping.get(char) and self._space_mapping.get(char).is_space:
                pass
            else:
                end = i + 1
        if len(text) > start:
            paragraphs.append(
                Token(content=text[start:len(text)], position=(start, len(text)), type="Paragraph", sub_tokens=[]))
        return paragraphs
