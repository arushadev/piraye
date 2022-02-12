# testing Fibonacci number function
# pylint: skip-file

from src.normalizer import Normalizer


def test_object():
    norm = Normalizer(['alphabet_fa'])
    assert norm is not None


def test_not_changing_input():
    text = "این یک متن فارسی ، English می‌باشد. این متن نباید تغییر کند.سال ۱۴۰۰ (1400)"
    norm = Normalizer([])
    assert text == norm.normalize(text)


def test_number():
    text = "1.2"
    norm = Normalizer().digit_fa().digit_en()
    assert text != norm.normalize(text)


def test_puncs():
    text = "شروع ، پایان"
    norm = Normalizer(['punc_en'])
    assert text != norm.normalize(text)
