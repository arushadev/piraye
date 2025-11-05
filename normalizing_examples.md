# Normalizing Examples

This document provides comprehensive examples of using Piraye's text normalization features.

## Basic Normalization

```python
from piraye import NormalizerBuilder
from piraye.tasks.normalizer.normalizer_builder import Config

text = "این یک متن تسة اسﺘ       , 24,12,1400 "

# Full normalization with all features
normalizer = NormalizerBuilder(
    [Config.PUNCTUATION_FA]).alphabet_fa().digit_fa().remove_extra_spaces().tokenizing().build()
normalized_text, result = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است ، ۲۴,۱۲,۱۴۰۰"
print(f"Shifts: {result.shifts}")
print(f"Punctuation positions: {result.punc_positions}")

# Without tokenizing
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).alphabet_fa().digit_fa().remove_extra_spaces().build()
normalized_text, _ = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است ، ۲۴، ۱۲، ۱۴۰۰ "

# Without remove_extra_spaces
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).alphabet_fa().digit_fa().tokenizing().build()
normalized_text, _ = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است       ، ۲۴,۱۲,۱۴۰۰ "

# Without changing digits
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).alphabet_fa().remove_extra_spaces().tokenizing().build()
normalized_text, _ = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است ، 24,12,1400 "

# Without modifying alphabets
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA]).digit_fa().tokenizing().remove_extra_spaces().build()
normalized_text, _ = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تسة اسﺘ ، ۲۴,۱۲,۱۴۰۰"

# Without changing punctuations
normalizer = NormalizerBuilder().alphabet_fa().digit_fa().remove_extra_spaces().tokenizing().build()
normalized_text, _ = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است , ۲۴,۱۲,۱۴۰۰"
```

## Diacritic Removal

```python
from piraye import NormalizerBuilder

# Delete diacritics and modify non-Persian alphabets
text = "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وآلِ مُحَمَّدٍ وعَجِّلْ فَرَجَهُمْ وسَهِّلْ مَخْرَجَهُمْ والعَنْ أعْدَاءَهُم"
normalizer = (NormalizerBuilder()
              .alphabet_fa()
              .diacritic_delete()
              .remove_extra_spaces()
              .tokenizing()
              .build())
normalized_text, result = normalizer.normalize(text)
print(normalized_text)  # "اللهم صل علی محمد وآل محمد وعجل فرجهم وسهل مخرجهم والعن اعداءهم"
```

## Working with Shifts and Punctuation

```python
from piraye import NormalizerBuilder

text = "Hello  ,  World  !  How are you?"
normalizer = (NormalizerBuilder()
              .alphabet_en()
              .punctuation_en()
              .space_normal()
              .remove_extra_spaces()
              .build())

normalized_text, result = normalizer.normalize(text)

print(f"Original: '{text}'")
print(f"Normalized: '{normalized_text}'")
print(f"\nShifts: {result.shifts}")
print(f"Punctuation positions: {result.punc_positions}")

# Show punctuation characters
for pos in result.punc_positions:
    char = normalized_text[pos]
    print(f"  Position {pos}: '{char}'")

# Map positions from normalized to original
if result.shifts:
    original_pos = normalizer.calc_original_position(result.shifts, 5)
    print(f"\nPosition 5 in normalized text was at position {original_pos} in original")
```

## Multi-Language Normalization

```python
from piraye import NormalizerBuilder

# Normalize mixed language text
text = "این یک test است! Hello, سلام"
normalizer = (NormalizerBuilder()
              .alphabet_fa()
              .alphabet_en()
              .punctuation_en()
              .punctuation_fa()
              .remove_extra_spaces()
              .build())

normalized_text, result = normalizer.normalize(text)
print(f"Original: '{text}'")
print(f"Normalized: '{normalized_text}'")
print(f"Punctuation at: {result.punc_positions}")
```

## Custom Configuration

```python
from piraye import NormalizerBuilder
from piraye.tasks.normalizer.normalizer_builder import Config

# Using specific configurations
normalizer = NormalizerBuilder(
    configs=[
        Config.ALPHABET_FA,
        Config.DIGIT_FA,
        Config.PUNCTUATION_FA,
        Config.SPACE_NORMAL,
        Config.DIACRITIC_DELETE
    ],
    remove_extra_spaces=True,
    tokenization=True
).build()

text = "این   یک  متن   است!  ۱۲۳"
normalized_text, result = normalizer.normalize(text)
print(normalized_text)
```

## Accessing NormalizationResult Properties

```python
from piraye import NormalizerBuilder

normalizer = (NormalizerBuilder()
              .alphabet_fa()
              .punctuation_fa()
              .digit_fa()
              .remove_extra_spaces()
              .build())

text = "سلام، این ۱۲۳ است."
normalized_text, result = normalizer.normalize(text)

# Access result properties
print(f"Normalized text: {normalized_text}")
print(f"Has shifts: {len(result.shifts) > 0}")
print(f"Number of punctuation marks: {len(result.punc_positions)}")
print(f"Shifts data: {result.shifts}")
print(f"Punctuation positions: {result.punc_positions}")

# Iterate over punctuation
for i, pos in enumerate(result.punc_positions, 1):
    char = normalized_text[pos]
    print(f"Punctuation {i}: '{char}' at position {pos}")
```