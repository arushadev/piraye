"""This module includes Tokenizer class for tokenizing texts"""

from typing import List, Tuple
from nltk import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer
import nltk
from .mappings import MappingDict
from .tokenizer import Tokenizer


class NltkTokenizer(Tokenizer):
    """
    A class for nltk tokenizing.
    ...
    Methods
    -------
    word_tokenize(text: str):
        return tokenized text
    sentence_tokenize(text: str):
        return sentence tokenized text
    """

    def __init__(self, ):
        """
            constructor
        """
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("downloading tokenizer data : ")
            nltk.download('punkt')
        self.__en_mapping = MappingDict.load_jsons(["digit_en", "punc_en"])

    def word_tokenize(self, text) -> List[str]:
        """
            Return a tokenized text.
            :param text: the input text
            :return: list of words
        """
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        spans = list(TreebankWordTokenizer().span_tokenize(text2))
        tokens = []
        for span in spans:
            tokens.append(text[span[0]:span[1]])
        return tokens

    def sentence_tokenize(self, text) -> List[str]:
        """
            Return a sentence tokenized text.
            :param text: the input text
            :return: list of sentences
        """
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        tokens_en = sent_tokenize(text2)
        return NltkTokenizer.__get_original_tokens(text, text2, tokens_en)

    def span_tokenize(self, text) -> List[Tuple[int, int, str]]:
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        spans = list(TreebankWordTokenizer().span_tokenize(text2))
        result = []
        for span in spans:
            result.append((span[0], span[1], text[span[0]:span[1]]))
        return result

    @staticmethod
    def __get_original_tokens(text: str, text2: str, tokens_en: List[str]) -> List[str]:
        text2_counter = 0
        tokens = []
        for token_en in tokens_en:
            try:
                token_index = text2.index(token_en, text2_counter)
                curr_text = text[token_index:token_index + len(token_en)]
                tokens.append(curr_text)
                text2_counter = token_index + len(token_en)
            except ValueError:
                tokens.append(token_en)
        return tokens
