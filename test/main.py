from normalizer import Normalizer

text = '.محمد   & حمزﻫ در , تاریخ ۲۴/12 به ("دانشگاهِ شریف") رفتند '
norm = Normalizer(['fa'], remove_extra_spaces=False)
result = norm.normalize(text)
print(result)
with open("output/Output.txt", "w") as text_file:
    text_file.write(result)
