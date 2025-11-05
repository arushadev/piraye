# Piraye: Advanced NLP Utilities for Persian, Arabic, and English

<p align="center">
  <a href="https://pypi.org/project/piraye"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/piraye.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/piraye"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/piraye.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/piraye"><img alt="License" src="https://img.shields.io/pypi/l/piraye.svg?maxAge=86400" /></a>
  <a href="https://pepy.tech/project/piraye"><img alt="Downloads" src="https://static.pepy.tech/badge/piraye" /></a>
</p>

---

**Piraye** is a Python library providing **flexible text normalization and tokenization utilities** for Persian, Arabic,
and English NLP tasks. With comprehensive type hints, extensive documentation, and a clean architecture, Piraye is
production-ready for modern NLP pipelines.

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start: Text Normalization](#-quick-start-text-normalization)
- [Position Mapping](#-position-mapping-after-normalization)
- [Configuration Options](#-configurations)
- [Tokenization Framework](#-tokenization-framework)
- [Built-in Tokenizers](#-built-in-tokenizers)
- [TokenizerPipeline](#-tokenizerpipeline-hierarchical-tokenization)
- [Project Structure](#-project-structure)
- [License](#-license)
- [Maintainers](#-maintainers)
- [Show Your Support](#-show-your-support)

---

## 🚀 Key Features

| Feature                          | Description                                                                                |
|----------------------------------|--------------------------------------------------------------------------------------------|
| **Multi-Language Normalization** | Normalize alphabets, digits, punctuation, and whitespace for Persian, Arabic, and English. |
| **Advanced Tokenization**        | Regex-based, NLTK-based, Spacy-based, and custom tokenizers with hierarchical support.     |
| **Tokenizer Pipeline**           | Chain multiple tokenizers for sophisticated text processing workflows.                     |
| **Position Tracking**            | Map positions between original and normalized text.                                        |
| **Multi-Lingual Detection**      | Automatic language detection and appropriate normalization.                                |
| **Type Safe**                    | Complete type hints for modern Python development.                                         |
| **Well Documented**              | Comprehensive documentation and usage examples.                                            |
| **Production Ready**             | Clean architecture, extensive testing, and easy integration.                               |

---

## 📦 Installation

### Basic Installation

```bash
pip install piraye 
```

### Full Installation (with Spacy support)

```bash
pip install piraye[full]
```

**Requirements**: Python 3.11+

---

## 🧠 Quick Start: Text Normalization

Normalize Persian text by correcting and standardizing letters, digits, and punctuation, performing tokenization,
and removing extra spaces to produce clean, consistent text ready for NLP processing.

### Basic Normalization (Builder Pattern)

```python
from piraye import NormalizerBuilder

text = "این یک متن تسة اسﺘ       , 24/12/1400 "
normalizer = (NormalizerBuilder()
              .alphabet_fa()
              .digit_fa()
              .punctuation_fa()
              .tokenizing()
              .remove_extra_spaces()
              .build())

# normalize() returns tuple: (normalized_text, NormalizationResult)
normalized_text, result = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است ، ۲۴/۱۲/۱۴۰۰"
print(result.shifts)  # Position shifts for mapping
print(result.punc_positions)  # Punctuation locations in normalized text
```

### Using Config Constructor

```python
from piraye import NormalizerBuilder
from piraye.tasks.normalizer.normalizer_builder import Config

text = "این یک متن تسة اسﺘ       , 24/12/1400 "
normalizer = NormalizerBuilder(
    configs=[Config.PUNCTUATION_FA, Config.ALPHABET_FA, Config.DIGIT_FA],
    remove_extra_spaces=True,
    tokenization=True
).build()

normalized_text, result = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است ، ۲۴/۱۲/۱۴۰۰"
```

> 📖 For more examples and usage patterns, see [Normalizer Examples](normalizing_examples.md).

---

## 📊 Normalizer Output

The `normalize()` method returns a tuple containing the normalized text and a `NormalizationResult` object with
metadata.

### Return Value Structure

```python
normalized_text, result = normalizer.normalize(text)
# Returns: tuple[str, NormalizationResult]
```

### NormalizationResult Properties

| Property         | Type                    | Description                                                                                           |
|------------------|-------------------------|-------------------------------------------------------------------------------------------------------|
| `shifts`         | `list[tuple[int, int]]` | Position shifts tracking character position changes during normalization. Format: `(position, shift)` |
| `punc_positions` | `list[int]`             | List of punctuation character positions in the normalized text                                        |

### Example

```python
from piraye import NormalizerBuilder

normalizer = (NormalizerBuilder()
              .alphabet_fa()
              .punctuation_fa()
              .digit_fa()
              .remove_extra_spaces()
              .build())

text = "سلام،  این  ۱۲۳  است."
normalized_text, result = normalizer.normalize(text)

# Normalized text
print(normalized_text)
# Output: "سلام، این ۱۲۳ است."

# Shifts for position mapping
print(result.shifts)
# Output: [(4, 0), (9, 1), (13, 2), (17, 3)]
# Each tuple represents (position_in_normalized_text, cumulative_shift_from_original)

# Punctuation positions
print(result.punc_positions)
# Output: [4, 17]
# Positions where punctuation characters (، and .) are located in normalized text

# Access individual punctuation characters
for pos in result.punc_positions:
    char = normalized_text[pos]
    print(f"Punctuation at position {pos}: '{char}'")
# Output:
# Punctuation at position 4: '،'
# Punctuation at position 17: '.'
```

---

## 🔢 Position Mapping After Normalization

When normalizing text, characters may be added, removed, or replaced. Piraye tracks these changes and provides utilities
to map positions between normalized and original text.

### Methods

| Method                                       | Description                                                          |
|----------------------------------------------|----------------------------------------------------------------------|
| `calc_original_position(shifts, position)`   | Returns the original position for a single index in normalized text. |
| `calc_original_positions(shifts, positions)` | Returns original positions for multiple indices (must be sorted).    |

### Example

```python
from piraye import NormalizerBuilder

normalizer = (NormalizerBuilder()
              .space_normal()
              .remove_extra_spaces()
              .alphabet_en()
              .punctuation_en()
              .build())

text = "Hello  ,  World  !"
normalized_text, result = normalizer.normalize(text)

# Access shifts from NormalizationResult
shifts = result.shifts
print(f"Shifts: {shifts}")

# Map single position
original_pos = normalizer.calc_original_position(shifts, 7)
print(f"Position 7 in normalized text was at position {original_pos} in original")

# Map multiple positions (must be sorted)
positions = [3, 7, 12]
original_positions = normalizer.calc_original_positions(shifts, positions)
print(f"Positions {positions} map to {original_positions} in original text")
```

### Working with Punctuation Positions

```python
from piraye import NormalizerBuilder

normalizer = (NormalizerBuilder()
              .alphabet_fa()
              .punctuation_fa()
              .build())

text = "سلام، این یک متن است."
normalized_text, result = normalizer.normalize(text)

# Access punctuation positions
print(f"Punctuation found at positions: {result.punc_positions}")

# Get the actual punctuation characters
punc_chars = [normalized_text[pos] for pos in result.punc_positions]
print(f"Punctuation characters: {punc_chars}")
```

> 💡 **Tip**: Use position mapping to align annotations, highlight text, or track character positions through
> normalization.

## ⚙️ Configurations

Piraye provides various configurations for text normalization:

|      Config      |     Function     |                     Description                     |
|:----------------:|:----------------:|:---------------------------------------------------:|
|   ALPHABET_AR    |   alphabet_ar    |         Maps alphabet characters to Arabic          |
|   ALPHABET_EN    |   alphabet_en    |         Maps alphabet characters to English         |
|   ALPHABET_FA    |   alphabet_fa    |         Maps alphabet characters to Persian         |
|     DIGIT_AR     |     digit_ar     |          Converts digits to Arabic digits           |
|     DIGIT_EN     |     digit_en     |          Converts digits to English digits          |
|     DIGIT_FA     |     digit_fa     |          Converts digits to Persian digits          |
| DIACRITIC_DELETE | diacritic_delete |               Removes all diacritics                |
|   SPACE_DELETE   |   space_delete   |                 Removes all spaces                  |
|   SPACE_NORMAL   |   space_normal   | Normalizes spaces (e.g., NO-BREAK SPACE, Tab, etc.) |
|    SPACE_KEEP    |    space_keep    |          Maps spaces and keeps them as-is           |
|  PUNCTUATION_AR  |  punctuation_ar  |      Maps punctuations to Arabic punctuations       |
|  PUNCTUATION_FA  |  punctuation_fa  |      Maps punctuations to Persian punctuations      |
|  PUNCTUATION_EN  |  punctuation_en  |      Maps punctuations to English punctuations      |

Other attributes:

* `remove_extra_spaces`: Collapses multiple consecutive spaces into a single space.
* `tokenization`: Converts punctuation characters into separate tokens.

---

## ✂️ Tokenization Framework

All tokenizers inherit from the `Tokenizer` abstract base class and produce `Token` objects with rich metadata.

### Token Structure

| Field        | Type              | Description                                              |
|--------------|-------------------|----------------------------------------------------------|
| `content`    | `str`             | The text content of the token.                           |
| `type`       | `str`             | The type or name of the tokenizer that created it.       |
| `position`   | `tuple[int, int]` | Start and end indices of the token in the original text. |
| `sub_tokens` | `List[Token]`     | A list of child tokens (for hierarchical tokenization).  |

### Base Methods

- **`tokenize(text: str) -> List[Token]`** – Main tokenization method
- **`merge(text: str, previous_tokens: List[Token]) -> List[Token]`** – Merge tokens hierarchically

---

## 🔤 Built-in Tokenizers

### NLTK-based Tokenizers

- **`NltkWordTokenizer`** – Word-level tokenization using NLTK
- **`NltkSentenceTokenizer`** – Sentence-level tokenization using Punkt algorithm

### Spacy-based Tokenizers

- **`SpacyWordTokenizer`** – Word-level tokenization using Spacy
- **`SpacySentenceTokenizer`** – Sentence-level tokenization using Spacy

### Regex-based Tokenizers

- **`RegexTokenizer`** – Generic regex pattern tokenizer
- **`URLTokenizer`** – Extract URLs from text
- **`EmailTokenizer`** – Extract email addresses from text
- **`HTMLTokenizer`** – Extract HTML tags from text

### Structural Tokenizers

- **`ParagraphTokenizer`** – Split text into paragraphs

---

## 🔄 TokenizerPipeline: Hierarchical Tokenization

The `TokenizerPipeline` class provides a modular and sequential approach to text tokenization. It allows you to chain
multiple tokenizers together, where the output of one tokenizer can be merged or refined by the next. This design makes
it easy to combine tokenizers (e.g., sentences, words, emojis, URLs) into a unified pipeline for flexible and powerful
text preprocessing.

### How It Works

The pipeline starts with the first tokenizer, which processes the raw text. Each subsequent tokenizer is applied
sequentially, refining or extending the previous tokens. The final result is a merged list of Token objects representing
a fully tokenized text.

### Example Usage

```python
from piraye.tasks.tokenizer import NltkSentenceTokenizer
from piraye.tasks.tokenizer import URLTokenizer
from piraye.tasks.tokenizer.pipeline import TokenizerPipeline

pipeline = TokenizerPipeline([
    NltkSentenceTokenizer(),
    URLTokenizer()
])
text = "Contact us at support@arusha.dev or info@piraye.ai."
tokens = pipeline(text)

print([t.content for t in tokens])

# ["Contact us at support@arusha.dev or info@piraye.ai."]
```

### Paragraph Tokenizer Example

```python
from piraye.tasks.tokenizer import ParagraphTokenizer

text = "First paragraph.\nSecond paragraph.\nThird paragraph."
tokenizer = ParagraphTokenizer()
tokens = tokenizer.tokenize(text)

for token in tokens:
    print(token)

# Token(content='First paragraph.', type='Paragraph', position=(0, 16), sub_tokens=[])
# Token(content='\nSecond paragraph.', type='Paragraph', position=(16, 34), sub_tokens=[]) 
# Token(content='\nThird paragraph.', type='Paragraph', position=(34, 51), sub_tokens=[])
```

> 📖 For more examples and usage patterns, see [Tokenizing Examples](tokenizing_examples.md).

---

## 📁 Project Structure

```
piraye/
├── piraye/
│   ├── __init__.py
│   ├── constants.py
│   └── tasks/
│       ├── normalizer/
│       │   ├── __init__.py
│       │   ├── char_config.py
│       │   ├── character_normalizer.py
│       │   ├── mappings.py
│       │   ├── multi_lingual_normalizer.py
│       │   ├── multi_lingual_normalizer_builder.py
│       │   ├── normalizer.py
│       │   ├── normalizer_builder.py
│       │   └── data/
│       │       ├── alphabets/
│       │       ├── digits/
│       │       ├── others/
│       │       └── puncs/
│       └── tokenizer/
│           ├── __init__.py
│           ├── pipeline.py
│           ├── token.py
│           └── tokenizers/
│               ├── __init__.py
│               ├── base_tokenizer.py
│               ├── nltk_tokenizer.py
│               ├── spacy_tokenizer.py
│               ├── regex_tokenizer.py
│               ├── paragraph_tokenizer.py
│               └── regex_tokenizers/
│                   ├── __init__.py
│                   ├── base_regex_tokenizer.py
│                   ├── url_tokenizer.py
│                   ├── email_tokenizer.py
│                   ├── html_tokenizer.py
│                   └── README.md
├── tests/
│   ├── test_normalizer.py
│   ├── test_ml_normalizer.py
│   ├── test_tokenizer.py
│   ├── test_tokenizer_pipeline.py
│   ├── test_html_tokenizer.py
│   └── ...
├── README.md
├── LICENSE
└── pyproject.toml
```

## 📄 License

**GNU Lesser General Public License v2.1**  
See [LICENSE](https://github.com/arushadev/piraye/blob/main/LICENSE)

---

## ❤️ Maintainers

Piraye is maintained by [Arusha](https://www.arusha.dev).

**Authors:**

- Hamed Khademi Khaledi
- HosseiN Khademi Khaledi
- Majid Asgari Bidhendi

For questions or support, please open an issue on GitHub or contact us at info@arusha.dev.

---

## 🌟 Show Your Support

If you find Piraye useful, please consider:

- ⭐ Starring the repository on GitHub
- 📢 Sharing it with others who might benefit
- 🐛 Reporting bugs or suggesting features
- 🤝 Contributing to the codebase

Thank you for using Piraye! 🎉
