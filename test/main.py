"""This module shows an example of how to use normalizer and test it"""
import os

from normalizer import Normalizer

TEXT = "الصراط المستقیم و الانزع البطین"
norm = Normalizer(["alphabet_fa", "space_normal"], False)
# norm.normalize(text)
result = norm.normalize(TEXT)
print(result)
if not os.path.exists('output'):
    os.mkdir('output')
with open("./output/output.txt", "w", encoding="utf-8") as text_file:
    text_file.write(result)
