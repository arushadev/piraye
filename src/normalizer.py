"""This module includes Normalizer class for normalizing texts"""
from __future__ import annotations

import json
import os
import string
import typing
from typing import Dict
from typing import List

from spacy.lang.en import English

from .char_config import CharConfig


class Normalizer:
    """
    A class for normalizer.

    ...

    Attributes
    ----------
    configs : List[str]
        list of desired configs
    remove_extra_spaces : bool
        that determines spaces stick together or not
    tokenization : bool
        tokenize text or not


    Methods
    -------
    normalize(text: str):
        get a text and normalize it and finally return it
    """

    def __init__(self, configs=None, remove_extra_spaces: bool = True, tokenization: bool = True):
        """
            constructor
            :param  configs : List[str]
                list of desired configs
            :param  remove_extra_spaces : bool
                that determines spaces stick together or not
            :param  tokenization : bool
                tokenize text or not
        """
        # Create a blank Tokenizer with just the English vocab
        if configs is None:
            configs = []
        self.__configs = configs
        self.__remove_extra_spaces = remove_extra_spaces
        if tokenization:
            self.__tokenizer = English().tokenizer
        else:
            self.__tokenizer = None
        self.__mapping: Dict[str, CharConfig] = {}
        self.__en_mapping: Dict[str, CharConfig] = {}
        self.__load_jsons()

    # pylint: disable=too-many-branches
    def normalize(self, text: str) -> str:
        """
            return a normalized text
            :param text: the input text
            :return: normalized text
        """

        if self.__tokenizer:
            is_token_list = self.__tokenize(text)
        else:
            is_token_list = [True] * len(text)
        result = ""
        last = None
        for i, char in enumerate(text):
            is_token = is_token_list[i]
            mapping_char = self.__mapping.get(char)
            if not self.__remove_extra_spaces:
                if mapping_char and \
                        (not mapping_char.is_token or (mapping_char.is_token and is_token)):
                    char = mapping_char.char
                result += char
            else:
                current = mapping_char if mapping_char else CharConfig(char)
                if current.is_space:
                    if last is None:
                        last = current
                    elif not last.is_space and last.space_after is not False:
                        last = current
                    elif last.is_space and current.space_priority < last.space_priority:
                        last = current
                else:
                    if last and last.is_space and last.space_before is not False:
                        result += last.char
                    # If last char is not space and need space before current or after last
                    if last and last.is_space is not True and \
                            (current.space_before or last.space_after) and is_token:
                        result += " "
                    if not current.is_token or (current.is_token and is_token):
                        result += current.char
                    else:
                        result += char
                    last = current
        if last and last.is_space:
            result += last.char
        return result

    def __tokenize(self, text: str) -> List[bool]:
        is_token_list = [False] * len(text)
        text2 = ''.join(
            [char if not self.__en_mapping.get(char)
             else self.__en_mapping.get(char).char for char in text])
        doc = self.__tokenizer(text2)
        text2_counter = 0
        for doc_i in doc:
            token = doc_i.text
            token_index = text2.index(token, text2_counter)
            if len(token) == 1:
                is_token_list[token_index] = True
            text2_counter = token_index + len(token)
        return is_token_list

    def __load_jsons(self):
        all_configs = []
        current_directory = os.path.dirname(os.path.abspath(__file__))
        for dir_path, _, filenames in os.walk(current_directory + "/data/"):
            for filename in filenames:
                all_configs.extend(Normalizer.read_json(os.path.abspath
                                                        (os.path.join(dir_path, filename))))
        self.__mapping = self.__get_mapping(self.__configs, all_configs)
        self.__en_mapping = self.__get_mapping(["digit_en", "punc_en"], all_configs)

    @staticmethod
    def __get_mapping(configs: List[str],
                      all_configs: List[Dict[str, typing.Any]]) -> Dict[str, CharConfig]:
        mapping = {}
        if configs and len(configs) == 0:
            return mapping
        for data in all_configs:
            for key in data["map"].keys():
                if key in configs:
                    key_map = data["map"][key]
                    mapping[key_map["char"]] = CharConfig.from_dict(data, key)
                    for char_dic in data["others"]:
                        char = char_dic["char"]
                        if not mapping.get(char):
                            mapping[char] = CharConfig.from_dict(data, key)
        return mapping

    @staticmethod
    def read_json(address: string):
        """
            return loaded json from dist
            :param address: the input address
            :return: loaded json
        """
        with open(address, encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data
