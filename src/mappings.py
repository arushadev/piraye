"""This module includes MappingDict class"""
import json
import os
import string
import typing

from typing import Dict
from typing import List

from .char_config import CharConfig


class MappingDict:
    """
    A class for mapping funcs.

    ...

    Attributes
    ----------
    Methods
    -------
    """

    @staticmethod
    def load_jsons(configs: List[str]) -> Dict[str, CharConfig]:
        """
            Mapping for configs and english configs from files
            :param configs: the input configs
            :return: mapping configs and mapping english
        """
        all_configs = []
        current_directory = os.path.dirname(os.path.abspath(__file__))
        for dir_path, _, filenames in os.walk(current_directory + "/data/"):
            for filename in filenames:
                abspath = os.path.abspath(os.path.join(dir_path, filename))
                all_configs.extend(MappingDict.read_json(abspath))

        return MappingDict.get_mapping(configs, all_configs)

    @staticmethod
    def get_mapping(configs: List[str],
                    all_configs: List[Dict[str, typing.Any]]) -> Dict[str, CharConfig]:
        """
            get mapping of desired configs
            :param configs: input configs
            :param all_configs: the all configs extracted from files
            :return: mapping char to char
        """
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
            return loaded json from files
            :param address: the input address
            :return: loaded json
        """
        with open(address, encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data
