"""Base class of tokenizer"""
from abc import ABC, abstractmethod
from typing import List, Tuple

from .tasks.normalizer.mappings import MappingDict


class Tokenizer(ABC):
    """
    Abstract class for tokenizing
    """

    def __init__(self):
        self._en_mapping = MappingDict.load_jsons(["digit_en", "punc_en"])
        self._space_mapping = MappingDict.load_jsons(["space_keep"])

    def word_tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into a list of words.
        :param text: The input text to tokenize.
        :return: A list of tokenized words.
        """
        tokens = self.word_span_tokenize(text)
        return [text for (_, _, text) in tokens]

    @abstractmethod
    def word_span_tokenize(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Tokenize the input text and return spans of the tokenized words.
        :param text: The input text to tokenize.
        :return: A list of tuples containing the start index, end index, and the tokenized word for each word span.
        """

    def sentence_tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into a list of sentences.
        :param text: The input text to tokenize.
        :return: A list of sentences.
        """
        tokens = self.sentence_span_tokenize(text)
        return [text for (_, _, text) in tokens]

    @abstractmethod
    def sentence_span_tokenize(self, text: str, clean_before_tokenize: bool = True) -> List[Tuple[int, int, str]]:
        """
        Tokenize the input text and return spans of the tokenized sentences.
        :param text: The input text to tokenize.
        :param clean_before_tokenize: clean and then tokenize it
        :return: A list of tuples containing the start index, end index, and the sentence for each sentence span.
        """

    def paragraph_tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into a list of paragraph.
        :param text: The input text to tokenize.
        :return: A list of paragraph.
        """
        tokens = self.paragraph_span_tokenize(text)
        return [text for (_, _, text) in tokens]

    def paragraph_span_tokenize(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Tokenize the input text and return spans of the tokenized paragraph.
        :param text: The input text to tokenize.
        :return: A list of tuples containing the start index, end index, and the sentence for each sentence span.
        """
        text2 = self._clean_text(text)
        text2_len = len(text2)
        sentences = self.sentence_span_tokenize(text2, False)
        paragraphs: List[Tuple[int, int, str]] = []
        last_index = 0
        for _, sentence_end, _ in sentences:
            if last_index + 1 >= text2_len:
                break
            pointer = sentence_end + 1
            while True:
                if pointer + 1 >= text2_len:
                    paragraphs.append((last_index, pointer, text[last_index:pointer]))
                    break
                character = text2[pointer]
                if character == "\n":
                    paragraphs.append((last_index, pointer, text[last_index:pointer]))
                    last_index = pointer + 1
                    break
                if character not in self._space_mapping or not self._space_mapping.get(character).is_space:
                    break
                pointer = pointer + 1
        return paragraphs

    def _clean_text(self, text: str) -> str:
        """
        Clean the input text by replacing digits and punctuation with normalized versions.
        :param text: He inputs text to clean.
        :return: The cleaned text with normalized digits and punctuation.
        """
        return ''.join(
            [char if not self._en_mapping.get(char)
             else self._en_mapping.get(char).char for char in text])
