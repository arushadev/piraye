# Piraye: Advanced NLP Utilities for Persian, Arabic, and English

<p align="center">
  <a href="https://pypi.org/project/piraye"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/piraye.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/piraye"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/piraye.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/piraye"><img alt="License" src="https://img.shields.io/pypi/l/piraye.svg?maxAge=86400" /></a>
  <a href="https://pepy.tech/project/piraye"><img alt="Downloads" src="https://static.pepy.tech/badge/piraye" /></a>
</p>

---

**Piraye** is a Python library providing **flexible text normalization and tokenization utilities** for Persian, Arabic, and English NLP tasks.

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **Text Normalization** | Normalize alphabets, digits, punctuation, and whitespace for multiple languages. |
| **Advanced Tokenization** | Supports regex-based, NLTK-based, Spacy-based, and custom tokenizers. |
| **Tokenizer Pipeline** | Sequentially combine multiple tokenizers for hierarchical tokenization. |
| **Extensible & Configurable** | Abstract base classes allow custom tokenizers and normalization. |
| **Production Ready** | Clean architecture, type hints, and easy integration in pipelines. |

---

## 🧩 Installation

```bash
pip install piraye spacy
python -m spacy download en_core_web_sm
```

---

## 🧠 Text Normalization Example

* Using builder pattern:

```python
from piraye import NormalizerBuilder

text = "این یک متن تسة اسﺘ       , 24/12/1400 "
normalizer = NormalizerBuilder().alphabet_fa().digit_fa().punctuation_fa().tokenizing().remove_extra_spaces().build()
normalizer.normalize(text)  # "این یک متن تست است ، ۲۴/۱۲/۱۴۰۰"
```

* Using constructor:

```python
from piraye import NormalizerBuilder
from piraye.tasks.normalizer.normalizer_builder import Config

text = "این یک متن تسة اسﺘ       , 24/12/1400 "
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA, Config.ALPHABET_FA, Config.DIGIT_FA], remove_extra_spaces=True,
                               tokenization=True).build()
normalizer.normalize(text)  # "این یک متن تست است ، ۲۴/۱۲/۱۴۰۰"
```
---

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
| DIACRITIC_DELETE | diacritic_delete |               Removes all diacritics               |
|   SPACE_DELETE   |   space_delete   |                 Removes all spaces                  |
|   SPACE_NORMAL   |   space_normal   | Normalizes spaces (e.g., NO-BREAK SPACE, Tab, etc.) |
|    SPACE_KEEP    |    space_keep    |         Maps spaces and keeps them as-is           |
|  PUNCTUATION_AR  |  punctuation_ar  |     Maps punctuations to Arabic punctuations       |
|  PUNCTUATION_Fa  |  punctuation_fa  |    Maps punctuations to Persian punctuations      |
|  PUNCTUATION_EN  |  punctuation_en  |     Maps punctuations to English punctuations      |

Other attributes:

* `remove_extra_spaces`: Appends multiple spaces together.  
* `tokenization`: Converts punctuation characters into separate tokens.

---

## ✂️ Tokenization Framework

All tokenizers inherit from `Tokenizer` and produce `Token` objects:

```python
from dataclasses import dataclass
from typing import List, Self

@dataclass(frozen=True)
class Token:
    content: str
    type: str
    position: tuple[int, int]
    sub_tokens: List[Self]

    def __str__(self):
        return f"Token(type={self.type}, content={self.content!r}, position={self.position}, sub_tokens={len(self.sub_tokens)})"
```

**Base methods**:

- `tokenize(text: str) -> List[Token]` – main tokenizer method.  
- `_clean_text(text: str)` – normalization before tokenizing.  
- `merge(text, previous_tokens)` – merge tokens hierarchically.  

---

## 🔤 Built-in Tokenizers

### NLTK-based
- `NltkWordTokenizer` – word-level  
- `NltkSentenceTokenizer` – sentence-level  

### Spacy-based
- `SpacyWordTokenizer` – word-level  
- `SpacySentenceTokenizer` – sentence-level  

### Regex-based
- `RegexTokenizer` – generic regex  
- `URLTokenizer` – extract URLs  
- `EmailTokenizer` – extract emails  

### Paragraph
- `ParagraphTokenizer` – split into paragraphs  

---

## ⚙️ Tokenizer Pipeline Example

```python
from piraye.tasks.tokenizer import TokenizerPipeline, SpacySentenceTokenizer, SpacyWordTokenizer

pipeline = TokenizerPipeline([
    SpacySentenceTokenizer(),
    SpacyWordTokenizer()
])

text = "Hello world! This is a test."
tokens = pipeline(text)
print([t.content for t in tokens])
# ['Hello', 'world', '!', 'This', 'is', 'a', 'test', '.']
```

---

## 🔧 Developer Guide

Create custom tokenizers by subclassing `Tokenizer`:

```python
import re

from piraye.tasks.tokenizer.regex_tokenizer import EmailTokenizer

tokenizer = EmailTokenizer()
text = "Please contact us at support@piraye.ai or info@piraye.io"
tokens = tokenizer.tokenize(text)
for token in tokens:
    print(token)
```

---

## 🧱 Project Structure

```
piraye/
├── tasks/
│   ├── normalizer/
│   └── tokenizer/
│       ├── base_tokenizer.py
│       ├── spacy_tokenizers.py
│       ├── nltk_tokenizers.py
│       ├── regex_tokenizers.py
│       ├── pipeline.py
│       └── token.py
├── utils/
│   └── mapping_dict.py
└── ...
```

---

## 🧩 Development Setup

```bash
git clone https://github.com/arushadev/piraye.git
cd piraye
pip install -e .[dev]
pytest
```

---

## 📄 License

**GNU Lesser General Public License v2.1**  
See [LICENSE](https://github.com/arushadev/piraye/blob/main/LICENSE)

---

## ❤️ Maintainer

Piraye is maintained by [Arusha](https://www.arusha.dev). Contributions welcome.
