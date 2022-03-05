# Examples

```python
from piraye import NormalizerBuilder
from piraye.normalizer_builder import Config

text = "این یک متن تسة اسﺘ       , 24,12,1400 "
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).alphabet_fa().digit_fa().remove_extra_spaces().tokenizing().build()
print(normalizer.normalize(text))  # "این یک متن تست است ، ۲۴,۱۲,۱۴۰۰"

# without tokenizing
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).alphabet_fa().digit_fa().remove_extra_spaces().build()
print(normalizer.normalize(text))  # "این یک متن تست است ، ۲۴، ۱۲، ۱۴۰۰ "

# without remove_extra_spaces
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).alphabet_fa().digit_fa().tokenizing().build()
print(normalizer.normalize(text))  # "این یک متن تست است       ، ۲۴,۱۲,۱۴۰۰ "

# without change digits (.digit_fa())
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).alphabet_fa().remove_extra_spaces().tokenizing().build()
print(normalizer.normalize(text))  # "این یک متن تست است ، 24,12,1400 "

# without modification alphabets (.alphabet_fa())
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).digit_fa().tokenizing().remove_extra_spaces().build()
print(normalizer.normalize(text))  # "این یک متن تسة اسﺘ ، ۲۴,۱۲,۱۴۰۰"

# without change punctuations (Config.PUNCTUATION_FA)
normalizer = NormalizerBuilder().alphabet_fa().digit_fa().remove_extra_spaces().tokenizing().build()
print(normalizer.normalize(text))  # "این یک متن تست است , ۲۴,۱۲,۱۴۰۰"
```

``` python
from piraye import NormalizerBuilder
# delete diacritics and modify non persian alphabets
text = "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وآلِ مُحَمَّدٍ وعَجِّلْ فَرَجَهُمْ وسَهِّلْ مَخْرَجَهُمْ والعَنْ أعْدَاءَهُم"
normalizer = NormalizerBuilder().alphabet_fa().diacritic_delete().remove_extra_spaces().tokenizing().build()
print(normalizer.normalize(text))  # "اللهم صل علی محمد وآل محمد وعجل فرجهم وسهل مخرجهم والعن اعداءهم"
```