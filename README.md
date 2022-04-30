# Piraye: NLP Utils

<p align="center">
  <a href="https://pypi.org/project/piraye"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/piraye.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/piraye"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/piraye.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/piraye"><img alt="License" src="https://img.shields.io/pypi/l/piraye.svg?maxAge=86400" /></a>
  <a href="https://github.com/arushadev/piraye/actions/workflows/pylint.yml"><img alt="Pylint" src="https://github.com/arushadev/piraye/actions/workflows/pylint.yml/badge.svg" /></a>
  <a href="https://github.com/arushadev/piraye/actions/workflows/unit-test.yml/badge.svg)](https://github.com/arushadev/piraye/actions/workflows/unit-test.yml"><img alt="Unit Test" src="https://github.com/arushadev/piraye/actions/workflows/unit-test.yml/badge.svg" /></a>
</p>


A utility for normalizing persian, arabic and english texts

## Requirements

* Python 3.9+
* nltk 3.4.5+

## Installation

Install the latest version with pip
`pip install piraye`

## Usage

Create an instance of Normalizer with NormalizerBuilder and then call normalize function. Also see list of all available
configs in [configs](#Configs) section.

* Using builder pattern:
```python
from piraye import NormalizerBuilder
from piraye.normalizer_builder import Config

text = "این یک متن تسة اسﺘ       , 24/12/1400 "
normalizer = NormalizerBuilder().alphabet_fa().digit_fa().punctuation_fa().tokenizing().remove_extra_spaces().build()
normalizer.normalize(text)  # "این یک متن تست است ، ۲۴/۱۲/۱۴۰۰"
```
* Using constructor:
```python
from piraye import NormalizerBuilder
from piraye.normalizer_builder import Config

text = "این یک متن تسة اسﺘ       , 24/12/1400 "
normalizer = NormalizerBuilder([Config.PUNCTUATION_FA, Config.ALPHABET_FA, Config.DIGIT_FA], remove_extra_spaces=True, tokenization=True).build()
normalizer.normalize(text)  # "این یک متن تست است ، ۲۴/۱۲/۱۴۰۰"
```

Also see [other examples](https://github.com/arushadev/piraye/blob/readme/examples.md)

## Configs

|      Config      |     Function     |                      Description                      |
|:----------------:|:----------------:|:-----------------------------------------------------:|
|   ALPHABET_AR    |   alphabet_ar    |         mapping alphabet characters to arabic         |
|   ALPHABET_EN    |   alphabet_en    |        mapping alphabet characters to english         |
|   ALPHABET_FA    |   alphabet_fa    |        mapping alphabet characters to persian         |
|     DIGIT_AR     |     digit_ar     |            convert digits to arabic digits            |
|     DIGIT_EN     |     digit_en     |           convert digits to english digits            |
|     DIGIT_FA     |     digit_fa     |           convert digits to persian digits            |
| DIACRITIC_DELETE | diacritic_delete |                 remove all diacritics                 |
|   SPACE_DELETE   |   space_delete   |                   remove all spaces                   |
|   SPACE_NORMAL   |   space_normal   | normal spaces ( like NO-BREAK SPACE , Tab and etc...) |
|    SPACE_KEEP    |    space_keep    |          mapping spaces and not normal them           |
|  PUNCTUATION_AR  |  punctuation_ar  |      mapping punctuations to arabic punctuations      |
|  PUNCTUATION_Fa  |  punctuation_fa  |     mapping punctuations to persian punctuations      |
|  PUNCTUATION_EN  |  punctuation_en  |     mapping punctuations to english punctuations      |

Other attributes:

* remove_extra_spaces : append multiple spaces together
* tokenization : replace punctuation characters that just are tokens

## License

**GNU Lesser General Public License v2.1**

Primarily used for software libraries, the GNU LGPL requires that derived works be licensed under the same license, but
works that only link to it do not fall under this restriction. There are two commonly used versions of the GNU LGPL.

See [LICENSE](https://github.com/arushadev/piraye/blob/main/LICENSE)

## About ️

[Arusha](https://www.arusha.dev)

