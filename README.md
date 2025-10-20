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
pip install piraye 
```

---

## 🧠 Text Normalization Example

Normalize Persian text by correcting and standardizing letters, digits, and punctuation, performing tokenization, 
and removing extra spaces to produce clean, consistent text ready for NLP processing.

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

> For more examples and usage patterns, please refer to the [Normalizer Examples](normalizing_examples.md).

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

| Field        | Type              | Description                                                         |
| ------------ | ----------------- | ------------------------------------------------------------------- |
| `content`    | `str`             | The text content of the token.                                      |
| `type`       | `str`             | The type or name of the tokenizer that created it.                  |
| `position`   | `tuple[int, int]` | Start and end indices of the token in the original text.            |
| `sub_tokens` | `List[Token]`     | A list of child tokens, if the token is composed of smaller tokens. |


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

🔄 TokenizerPipeline

The TokenizerPipeline class provides a modular and sequential approach to text tokenization.
It allows you to chain multiple tokenizers together, where the output of one tokenizer can be merged or refined by the next.
This design makes it easy to combine tokenizers (e.g., sentences, words, emojis, URLs) into a unified pipeline for flexible and powerful text preprocessing.

🧠 How It Works

The pipeline starts with the first tokenizer, which processes the raw text.
Each subsequent tokenizer is applied sequentially, refining or extending the previous tokens.
The final result is a merged list of Token objects representing a fully tokenized text.

## ⚙️ Tokenizer Pipeline Example (Sentence & URL)
 
```python
from piraye.tasks.tokenizer.spacy_tokenizer import  SpacySentenceTokenizer
from piraye.tasks.tokenizer.regex_tokenizer import  URLTokenizer
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

## ⚙️ Paragraph Tokenizer Pipeline Example

```python
from piraye.tasks.tokenizer.paragraph_tokenizer import ParagraphTokenizer

text = "First paragraph.\nSecond paragraph.\nThird paragraph."
tokenizer = ParagraphTokenizer()
tokens = tokenizer.tokenize(text)

for token in tokens:
    print(token)

#Token(content='First paragraph.', type='Paragraph', position=(0, 16), sub_tokens=[])
#Token(content='\nSecond paragraph.', type='Paragraph', position=(16, 34), sub_tokens=[]) 
#Token(content='\nThird paragraph.', type='Paragraph', position=(34, 51), sub_tokens=[])
```

> For more examples and usage patterns, please refer to the [Tokenizing Examples](tokenizing_examples.md).

---

## 🧱 Project Structure

```
piraye/
├── tasks/
│   ├── normalizer/
│   └── tokenizer/
└── ...
```

---

## 🧩 Development Setup

```bash
git clone https://github.com/arushadev/piraye.git
cd piraye
uv sync
```

---

## 📄 License

**GNU Lesser General Public License v2.1**  
See [LICENSE](https://github.com/arushadev/piraye/blob/main/LICENSE)

---

## ❤️ Maintainer

Piraye is maintained by [Arusha](https://www.arusha.dev). Contributions welcome.
