import json
import logging
import re
import string
from typing import List

from spacy.lang.en import English


class Normalizer:

    def __init__(self, langs: List[str], remove_extra_spaces=True, remove_diacritics=True):
        """
            constructor
            :param langs: a list of [fa,ar,en]
        """
        # Create a blank Tokenizer with just the English vocab
        self.__tokenizer = English().tokenizer
        self.__langs = langs
        self.__remove_extra_spaces = remove_extra_spaces
        self.__remove_diacritics = remove_diacritics
        self._init_data()

    def normalize(self, text: str) -> str:
        """
            return a incredible text
            :param text: the input text
            :return: normalized text
        """
        tokens = self.__tokenize(text)
        result = ' '.join(map(self.__mapping_token, tokens))
        if self.__remove_extra_spaces:
            result = self.__do_remove_extra_spaces(result)
        if self.__remove_diacritics:
            result = self.__do_remove_diacritics(result)
        return result

    def __tokenize(self, text: str) -> List[str]:
        text2 = self.__en_mapping_pd(text)
        doc = self.__tokenizer(text2)
        tokens = []
        text2_counter = 0
        for i in range(len(doc)):
            token = doc[i].text
            token_index = text2.index(token, text2_counter)
            tokens.append(text[token_index:token_index + len(token)])
            text2_counter = token_index + len(token)
        return tokens

    def __mapping_char_en(self, char):
        if char in self.__digits.keys():
            return self.__digits[char]['en']
        elif char in self.__puncs.keys():
            return self.__puncs[char]['en']
        return char

    def __en_mapping_pd(self, text: string) -> string:
        """
                mapping punctuations and digits to english
                :param text: input text
                :return: mapped text
        """
        return ''.join(map(self.__mapping_char_en, text))

    def __mapping_char(self, char):
        if char in self.__acceptable_chars:
            return char
        if char in self.__digits.keys():
            return self.__digits[char][self.__langs[0]]
        for lang in self.__langs[::-1]:
            if char in self.__letters[lang].keys():
                return self.__letters[lang][char]
        return char

    def __mapping_token(self, token):
        if token in self.__puncs.keys():
            return self.__puncs[token][self.__langs[0]]
        return ''.join(map(self.__mapping_char, token))

    def __do_remove_extra_spaces(self, text: string) -> string:
        """
        replace extra spaces with one space ( also for half space )
        :param text: a string
        :return: a string without extra spaces
        """
        res = ''.join([" " if char in self.__spaces.keys() else char for char in text])
        text = res
        # remove extra spaces
        text = re.sub(r' {2,}', ' ', text)
        # remove extra newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # remove extra ZWNJs
        text = re.sub(r'\u200c{2,}', '\u200c', text)
        # remove keshide, carriage returns
        text = re.sub(r'[ـ\r]', '', text)
        return text

    def __do_remove_diacritics(self, text: string) -> string:
        """
        remove all diacritics like ِ ُ َ
        :param text : a string
        :return: result
        """

        res = ''.join([" " if char in self.__diacritics.keys() else char for char in text])
        text = res
        text = text.replace("ِ", "")
        return text

    def _init_data(self):
        self.__letters = {'fa': [], 'ar': [], 'en': []}
        self.__puncs, self.__all_puncs = Normalizer.others_dic(
            Normalizer.read_json('./data/Punctuations/punctuations_edited.json'))
        self.__digits, self.__all_digits = Normalizer.others_dic(
            Normalizer.read_json('./data/Digits/digits.json'))
        self.__letters['fa'], self.__all_letters_fa = Normalizer.read_dics(
            Normalizer.read_json('./data/Characters/Persian/fa_alphabet.json'))
        self.__letters['en'], self.__all_letters_en = Normalizer.read_dics(
            Normalizer.read_json('./data/Characters/English/en_alphabet.json'))
        self.__letters['ar'], self.__all_letters_ar = Normalizer.read_dics(
            Normalizer.read_json('./data/Characters/Arabic/ar_alphabet.json'))
        self.__acceptable_chars = self.__create_acceptable_chars()
        self.__spaces, self.__all_spaces = Normalizer.read_dics(
            Normalizer.read_json('./data/Spaces/spaces.json'))
        self.__diacritics, self.__all_diacritics = Normalizer.read_dics(
            Normalizer.read_json('./data/Diacritic/diacritics.json'))

    def __create_acceptable_chars(self) -> list:

        result = []
        self.__all_chars = self.__all_puncs
        self.__all_chars = Normalizer.append_dics(
            dic1=self.__all_chars, dic2=self.__all_digits)
        self.__all_chars['fa'].extend(self.__all_letters_fa)
        self.__all_chars['en'].extend(self.__all_letters_en)
        self.__all_chars['ar'].extend(self.__all_letters_ar)
        for lang in self.__langs:
            result.extend(self.__all_chars[lang])
        return result

    @staticmethod
    def append_dics(dic1: dict, dic2: dict) -> dict:
        for key in dic1:
            dic1[key].extend(dic2[key])
        return dic1

    @staticmethod
    # read json file based on address
    def read_json(address: string):
        f = open(address, )
        data = json.load(f)
        return data

    @staticmethod
    def others_dic(data: dict):
        result = {}
        acceptable_chars = {'fa': [], 'en': [], 'ar': []}
        for _, value in data.items():
            for key in acceptable_chars:
                acceptable_chars[key].append(value[key]['char'])
            for ch in value['others']:
                try:
                    result[ch['char']] = {
                        'fa': value['fa']['char'],
                        'ar': value['ar']['char'],
                        'en': value['en']['char'],
                    }
                except Exception as e:
                    logging.exception(e)
                    print(ch['char'])
                    result[ch['char']] = {
                        'fa': value['fa'],
                        'ar': value['ar'],
                        'en': value['en'],
                    }

        return result, acceptable_chars

    @staticmethod
    def read_dics(data: dict):
        result = {}
        for key, value in data.items():
            for ch in value:
                try:
                    result[ch] = key
                except Exception as e:
                    logging.exception(e)
                    print('error : ', ch['char'])
        return result, data.keys()
