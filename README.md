# Piraye: NLP Utilities

<p align="center">
  <a href="https://pypi.org/project/piraye"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/piraye.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/piraye"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/piraye.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/piraye"><img alt="License" src="https://img.shields.io/pypi/l/piraye.svg?maxAge=86400" /></a>
  <a href="https://pepy.tech/project/piraye"><img alt="Downloads" src="https://static.pepy.tech/badge/piraye" /></a>
  <a href="https://github.com/arushadev/piraye/actions/workflows/pylint.yml"><img alt="Pylint" src="https://github.com/arushadev/piraye/actions/workflows/pylint.yml/badge.svg" /></a>
  <a href="https://github.com/arushadev/piraye/actions/workflows/unit-test.yml/badge.svg)](https://github.com/arushadev/piraye/actions/workflows/unit-test.yml"><img alt="Unit Test" src="https://github.com/arushadev/piraye/actions/workflows/unit-test.yml/badge.svg" /></a>
</p>


**Piraye** is a Python library designed to facilitate text normalization for Persian, Arabic, and English languages.

## Requirements

* Python 3.11+
* nltk 3.4.5+

## Installation

You can install the latest version of Piraye via pip:

`pip install piraye`

## Usage

To use Piraye, create an instance of the Normalizer class with NormalizerBuilder and then call the normalize function. You can configure the normalization process using various settings available. Below are two examples demonstrating different approaches:

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

You can find more examples [here](https://github.com/arushadev/piraye/blob/readme/examples.md)

## Configs

Piraye provides various configurations for text normalization. Here's a list of available configurations:

|      Config      |     Function     |                      Description                      |
|:----------------:|:----------------:|:-----------------------------------------------------:|
|   ALPHABET_AR    |   alphabet_ar    |         mapping alphabet characters to Arabic         |
|   ALPHABET_EN    |   alphabet_en    |        mapping alphabet characters to English         |
|   ALPHABET_FA    |   alphabet_fa    |        mapping alphabet characters to Persian         |
|     DIGIT_AR     |     digit_ar     |            convert digits to Arabic digits            |
|     DIGIT_EN     |     digit_en     |           convert digits to English digits            |
|     DIGIT_FA     |     digit_fa     |           convert digits to Persian digits            |
| DIACRITIC_DELETE | diacritic_delete |                 remove all diacritics                 |
|   SPACE_DELETE   |   space_delete   |                   remove all spaces                   |
|   SPACE_NORMAL   |   space_normal   | normal spaces ( like NO-BREAK SPACE , Tab and etc...) |
|    SPACE_KEEP    |    space_keep    |          mapping spaces and not normal them           |
|  PUNCTUATION_AR  |  punctuation_ar  |      mapping punctuations to Arabic punctuations      |
|  PUNCTUATION_Fa  |  punctuation_fa  |     mapping punctuations to Persian punctuations      |
|  PUNCTUATION_EN  |  punctuation_en  |     mapping punctuations to English punctuations      |

Other attributes:

* remove_extra_spaces: Appends multiple spaces together.
* tokenization: Replaces punctuation characters which are just tokens.

## Development

To set up a development environment, install dependencies with:

`pip install -e .[dev]`

## License

**GNU Lesser General Public License v2.1**

Piraye is licensed under the GNU Lesser General Public License v2.1, which primarily applies to software libraries.
See the [LICENSE](https://github.com/arushadev/piraye/blob/main/LICENSE) file for more details.

## About ️

Piraye is maintained by [Arusha](https://www.arusha.dev).


