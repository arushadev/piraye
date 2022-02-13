# testing Fibonacci number function
# pylint: skip-file

from src.normalizer import Normalizer
from src.normalizer_configuration import NormalizerConfiguration


def test_object():
    norm = NormalizerConfiguration().build()
    assert norm is not None


def test_not_changing_input():
    text = "این یک متن فارسی ، English می‌باشد. این متن نباید تغییر کند.سال ۱۴۰۰ (1400)"
    norm = NormalizerConfiguration().build()
    assert text == norm.normalize(text)


def test_number():
    text = "1.2"
    norm = NormalizerConfiguration().digit_fa().build()
    assert text != norm.normalize(text)


def test_puncs():
    text = "شروع ، پایان"
    norm = NormalizerConfiguration().punctuation_en().build()
    assert text != norm.normalize(text)
