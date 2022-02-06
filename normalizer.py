"""This module includes Normalizer class for normalizing texts"""
import json
import os
import re
import string
import typing
from typing import List

from spacy.lang.en import English


class Normalizer:
    """
    A class for normalizer.

    ...

    Attributes
    ----------
    configs : List[str]
        list of desired configs
    remove_extra_spaces : boo
        that determines spaces stick together or not


    Methods
    -------
    normalize(text: str):
        get a text and normalize it and finally return it
    """

    def __init__(self, configs: List[str], remove_extra_spaces: bool = True):
        """
            constructor
            :param configs
        """
        # Create a blank Tokenizer with just the English vocab
        self.__tokenizer = English().tokenizer
        self.__configs = configs
        self.__remove_extra_spaces = remove_extra_spaces
        self.__mapping, self.__mapping_punc, self.__en_mapping = self.__load_jsons()

    def normalize(self, text: str) -> str:
        """
            return an incredible text
            :param text: the input text
            :return: normalized text
        """
        text = self.__change_puncs(text)
        result = ''.join([self.__mapping.get(char, char) for char in text])
        if self.__remove_extra_spaces:
            result = Normalizer.do_remove_extra_spaces(result)
        return result

    def __change_puncs(self, text: str) -> str:
        text2 = ''.join([self.__en_mapping.get(char, char) for char in text])
        doc = self.__tokenizer(text2)
        text2_counter = 0
        final_text = ""
        last_token_index = 0
        prev_token = ""
        for doc_i in doc:
            token = doc_i.text
            token_index = text2.index(token, text2_counter)
            if last_token_index + len(prev_token) <= token_index:
                final_text += text[last_token_index + len(prev_token):token_index]
            curr_text = text[token_index:token_index + len(token)]
            if len(token) == 1 and self.__mapping_punc.get(curr_text):
                final_text += self.__mapping_punc[curr_text]
            else:
                final_text += curr_text
            text2_counter = token_index + len(token)
            last_token_index = token_index
            prev_token = token
        return final_text

    def __load_jsons(self) -> (dict[str, str], dict[str, str], dict[str, str]):
        all_configs = []
        current_directory = os.path.dirname(os.path.abspath(__file__))
        for dir_path, _, filenames in os.walk(current_directory + "/data/"):
            for filename in filenames:
                all_configs.extend(Normalizer.read_json(os.path.abspath
                                                        (os.path.join(dir_path, filename))))
        configs_punc = []
        configs_not_punc = []
        for config in self.__configs:
            if config.startswith("punc"):
                configs_punc.append(config)
            else:
                configs_not_punc.append(config)
        return Normalizer.__get_mapping(all_configs, configs_not_punc), \
               Normalizer.__get_mapping(all_configs, configs_punc), \
               Normalizer.__get_mapping(all_configs, ["digit_en", "punc_en"])

    @staticmethod
    def __get_mapping(all_configs: List[dict[str, typing.Any]],
                      configs: List[str]) -> dict[str, str]:
        mapping = {}
        for data in all_configs:
            for key in data["map"].keys():
                if key in configs:
                    mapping[data["map"][key]["char"]] = data["map"][key]["char"]
                    for char_dic in data["others"]:
                        char = char_dic["char"]
                        if not mapping.get(char):
                            mapping[char] = data["map"][key]["char"]

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

    @staticmethod
    def do_remove_extra_spaces(text: string) -> string:
        """
        replace extra spaces with one space ( also for half space )
        :param text: a string
        :return: a string without extra spaces
        """
        # remove extra spaces
        text = re.sub(r' {2,}', ' ', text)
        # remove extra newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # remove extra ZWNJs
        text = re.sub(r'\u200c{2,}', '\u200c', text)
        # remove keshide, carriage returns
        text = re.sub(r'[ـ\r]', '', text)
        return text
