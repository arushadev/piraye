"""Paragraph tokenizer implementation."""
from typing import List

from .base_tokenizer import Tokenizer
from ..token import Token


# pylint: disable=too-few-public-methods
class ParagraphTokenizer(Tokenizer):
    """
    Tokenizer that splits text into paragraphs based on newline characters.
    
    Paragraphs are identified by newline separators, with leading/trailing
    spaces handled appropriately.
    """

    def __init__(self):
        Tokenizer.__init__(self)

    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize text into paragraphs.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of Token objects representing paragraphs
        """
        if not text:
            return []

        start = 0
        end = 0
        paragraphs: List[Token] = []

        for i, char in enumerate(text):
            if char == "\n":
                if end > start:
                    paragraphs.append(
                        Token(
                            content=text[start:end],
                            position=(start, end),
                            type="Paragraph",
                            sub_tokens=[]
                        )
                    )
                    start = end
            elif self._space_mapping.get(char) and self._space_mapping.get(char).is_space:
                # Skip space characters when determining paragraph boundaries
                pass
            else:
                end = i + 1

        # Add remaining text as final paragraph
        if len(text) > start:
            paragraphs.append(
                Token(
                    content=text[start:len(text)],
                    position=(start, len(text)),
                    type="Paragraph",
                    sub_tokens=[]
                )
            )

        return paragraphs
