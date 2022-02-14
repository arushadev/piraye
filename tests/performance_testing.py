"""This module is for compare hazm and this normalizer"""
import time
import hazm
from tqdm import tqdm
from src.normalizer import Normalizer

if __name__ == '__main__':
    with open('./input/text.txt', encoding="utf-8") as f:
        text = f.read()
        norm = Normalizer(["alphabet_fa", "space_normal"], False)
        start = time.time()
        for i in tqdm(range(1000)):
            result = norm.normalize(text)
        end = time.time()
        print("ME : ", end - start)
        with open("./output/Output1.txt", "w", encoding="utf-8") as text_file:
            text_file.write(result)
        start2 = time.time()
        normalizer_hazm = hazm.Normalizer()
        for i in tqdm(range(1000)):
            result2 = normalizer_hazm.normalize(text)
        end2 = time.time()
        print("Hazm : ", end2 - start2)
        with open("./output/Output2.txt", "w", encoding="utf-8") as text_file:
            text_file.write(result2)
