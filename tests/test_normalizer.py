# testing Fibonacci number function
# pylint: skip-file

from ..piraye import NltkTokenizer
from ..piraye import NormalizerBuilder


def test_object():
    norm = NormalizerBuilder().build()
    assert norm is not None


def test_not_changing_input():
    text = "این یک متن فارسی ، English می‌باشد. این متن نباید تغییر کند.سال ۱۴۰۰ (1400)"
    norm = NormalizerBuilder().build()
    assert text == norm.normalize(text)


def test_number():
    text = "1.2"
    norm = NormalizerBuilder().digit_fa().build()
    assert text != norm.normalize(text)


def test_puncs():
    text = "شروع ، پایان"
    norm = NormalizerBuilder().punctuation_en().build()
    assert text != norm.normalize(text)


def test_space():
    text = "Hello  , Piraye(   NLP Tool   )  .  \n   \n"
    norm = NormalizerBuilder().remove_extra_spaces().alphabet_en().punctuation_en().build()
    assert "Hello, Piraye (NLP Tool).\n" != norm.normalize(text)


def test_quotes():
    text = "«"
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    norm.normalize(text)
    text = " «««« تست "
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    norm.normalize(text)
    text = " \" تست '' تست «««« تست "
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    norm.normalize(text)


def test_normalizer():
    tokens = NltkTokenizer().word_tokenize('\'\'Y\'"')
    print(tokens)
