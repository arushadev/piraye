"""This module is for compare hazm and this normalizer"""
import time

import hazm
from tqdm import tqdm

from src import NormalizerBuilder

if __name__ == '__main__':
    with open('./input.txt', encoding="utf-8") as f:
        text = f.read()
        norm = NormalizerBuilder() \
            .alphabet_fa().alphabet_en() \
            .digit_fa().punctuation_fa().diacritic_delete() \
            .space_normal().tokenizing().remove_extra_spaces() \
            .build()
        start = time.time()
        for i in tqdm(range(1)):
            result = norm.normalize(text)
        end = time.time()
        print("ME : ", end - start)
        with open("./output_piraye.txt", "w", encoding="utf-8") as text_file:
            text_file.write(result)
        start2 = time.time()
        normalizer_hazm = hazm.Normalizer()
        for i in tqdm(range(1)):
            result2 = normalizer_hazm.normalize(text)
        end2 = time.time()
        print("Hazm : ", end2 - start2)
        with open("./output_hazm.txt", "w", encoding="utf-8") as text_file:
            text_file.write(result2)
