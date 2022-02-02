import json
import os
import re
import string
from typing import List

from spacy.lang.en import English


class Normalizer:

    def __init__(self, configs: List[str], remove_extra_spaces=True):
        """
            constructor
            :param configs
        """
        langs: List[str]
        # Create a blank Tokenizer with just the English vocab
        self.__tokenizer = English().tokenizer
        self.__configs = configs
        self.__remove_extra_spaces = remove_extra_spaces
        self.__mapping, self.__mapping_punc, self.__en_mapping = self.__load_jsons()
        self.__tokens = []

    def __mapping_char(self, char):
        if char in self.__mapping.keys():
            return self.__mapping[char]
        return char

    def normalize(self, text: str) -> str:
        """
            return an incredible text
            :param text: the input text
            :return: normalized text
        """
        text = self.__change_puncs(text)
        result = ''.join(map(self.__mapping_char, text))
        if self.__remove_extra_spaces:
            result = Normalizer.do_remove_extra_spaces(result)
        return result

    def __change_puncs(self, text: str) -> str:
        text2 = ''.join([self.__en_mapping[char] if char in self.__en_mapping.keys() else char for char in text])
        doc = self.__tokenizer(text2)
        text2_counter = 0
        final_text = ""
        last_token_index = 0
        prev_token = ""
        for i in range(len(doc)):
            token = doc[i].text
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
            for f in filenames:
                all_configs.extend(Normalizer.read_json(os.path.abspath(os.path.join(dir_path, f))))
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
    def __get_mapping(all_configs: List[dict[str,]], configs: List[str]) -> dict[str, str]:
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
    # read json file based on address
    def read_json(address: string):
        f = open(address, )
        data = json.load(f)
        f.close()
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
