from normalizer import Normalizer

text = "الصراط المستقیم و الانزع البطین"
norm = Normalizer(["alphabet_fa", "space_normal"], False)
# norm.normalize(text)
result = norm.normalize(text)
print(result)
with open("./output/output.txt", "w") as text_file:
    text_file.write(result)
