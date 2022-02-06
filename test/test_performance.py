from normalizer import Normalizer
import time
import hazm
from tqdm import tqdm

if __name__ == '__main__':
    with open('./input/text.txt') as f:
        text = f.read()
        norm = Normalizer(["alphabet_fa", "space_normal"], False)
        start = time.time()
        for i in tqdm(range(1000)):
            result = norm.normalize(text)
        end = time.time()
        print("ME : ", end - start)
        with open("./output/Output1.txt", "w") as text_file:
            text_file.write(result)
        start2 = time.time()
        Normalizer = hazm.Normalizer()
        for i in tqdm(range(1000)):
            result2 = Normalizer.normalize(text)
        end2 = time.time()
        print("Hazm : ", end2 - start2)
        with open("./output/Output2.txt", "w") as text_file:
            text_file.write(result2)
