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

# normalize() returns tuple: (normalized_text, position_shifts)
normalized_text, shifts = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است ، ۲۴/۱۲/۱۴۰۰"
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

normalized_text, shifts = normalizer.normalize(text)
print(normalized_text)  # "این یک متن تست است ، ۲۴/۱۲/۱۴۰۰"
```

### Multi-Lingual Normalization

```python
from piraye import MultiLingualNormalizerBuilder

# Automatically detect and normalize Persian, Arabic, and English
normalizer = (MultiLingualNormalizerBuilder()
              .word_level()  # Detect language at word level
              .main_normalizer_lang('fa')  # Use Persian as main language
              .build())

text = "این یک test است with English words و کلمات عربی"
normalized_text, shifts = normalizer.normalize(text)
print(normalized_text)
```

> 📖 For more examples and usage patterns, see [Normalizer Examples](normalizing_examples.md).

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

normalizer = NormalizerBuilder().space_normal().remove_extra_spaces().alphabet_en().punctuation_en().build()

# Shifts calculated by the normalizer: (position_in_normalized, shift_value)
shifts = [(5, 2), (10, 1)]

# Map single position
original_pos = normalizer.calc_original_position(shifts, 7)
print(original_pos)
# 9

# Map multiple positions
positions = [3, 7, 12]
original_positions = normalizer.calc_original_positions(shifts, positions)
print(original_positions)
# [3, 9, 13]
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
from piraye.tasks.tokenizer import SpacySentenceTokenizer
from piraye.tasks.tokenizer import URLTokenizer
from piraye.tasks.tokenizer.pipeline import TokenizerPipeline

pipeline = TokenizerPipeline([
    SpacySentenceTokenizer(),
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
│               └── paragraph_tokenizer.py
├── tests/
│   ├── test_normalizer.py
│   ├── test_ml_normalizer.py
│   ├── test_tokenizer.py
│   ├── test_tokenizer_pipeline.py
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
