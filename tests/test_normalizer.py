# testing Fibonacci number function
# pylint: skip-file
import pytest

from ..piraye import SpacyWordTokenizer
from ..piraye import NormalizerBuilder


def test_object():
    norm = NormalizerBuilder().build()
    assert norm is not None


def test_not_changing_input():
    text = "این یک متن فارسی ، English می‌باشد. این متن نباید تغییر کند.سال ۱۴۰۰ (1400)"
    norm = NormalizerBuilder().build()
    assert text == norm.normalize(text)[0]


def test_number():
    text = "1.2"
    norm = NormalizerBuilder().digit_fa().build()
    assert text != norm.normalize(text)


def test_number_tokenize():
    text = "1,200 , "
    norm = NormalizerBuilder().punctuation_fa().tokenizing().build()
    assert "1,200 ، " == norm.normalize(text)[0]

def test_add_space_after_comma():
    text = "i,am"
    norm = NormalizerBuilder().space_normal().remove_extra_spaces().alphabet_en().punctuation_en().build()
    #assert "Hello, Piraye (NLP Tool).\n" != norm.normalize(text)
    assert "i, am" == norm.normalize(text)[0]
    # text1 = "Hello  , Piraye (   NLP Tool   )  .  \n   \n"
    # norm = NormalizerBuilder().remove_extra_spaces().alphabet_en().punctuation_en().build()
    # assert "Hello , Piraye (NLP Tool ) .\n" == norm.normalize(text1)

def test_space():
    text = "Hello  ,Piraye(   NLP Tool   )  .  \n   \n"
    norm = NormalizerBuilder().space_normal().remove_extra_spaces().alphabet_en().punctuation_en().build()
    #assert "Hello, Piraye (NLP Tool).\n" != norm.normalize(text)
    assert "Hello , Piraye (NLP Tool ) .\n" == norm.normalize(text)[0]
    # text1 = "Hello  , Piraye (   NLP Tool   )  .  \n   \n"
    # norm = NormalizerBuilder().remove_extra_spaces().alphabet_en().punctuation_en().build()
    # assert "Hello , Piraye (NLP Tool ) .\n" == norm.normalize(text1)

def test_shift():
    text = "0,3  5 \t\n.9.x.y.z"
    norm = NormalizerBuilder().space_normal().remove_extra_spaces().alphabet_en().punctuation_en().build()
    text2, shifts = norm.normalize(text)
    # assert "0, 3 5\n. 9. x. y. z" == text2
    # assert [(3, -1), (5, 0), (7, 2), (9, 1), (12, 0), (15, -1), (18, -2)] == shifts
    # assert norm.calc_original_position(shifts, 3) == 2
    # assert norm.calc_original_position(shifts, 13) == 13
    # assert norm.calc_original_position(shifts, 15) == 14
    # assert norm.calc_original_position(shifts, 19) == 17
    assert norm.calc_original_positions(shifts, [3, 13, 15, 19]) == [2, 13, 14, 17]
    with pytest.raises(Exception) as e:  # یا نوع خاص خطا مثل ValueError
        norm.calc_original_positions(shifts, [13, 3, 15, 19])
        assert str(e.value) == "The position list is not sorted"


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


def test_quotes_spacy():
    tokenizer = SpacyWordTokenizer()
    text = "«"
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().tokenizing(tokenizer=tokenizer).build()
    assert "\"" == norm.normalize(text)[0]
    text = " «««« تست "
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    assert ' """" تست ' == norm.normalize(text)[0]
    text = " \" تست '' تست «««« تست "
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    assert ' " تست \'\' تست """" تست ' == norm.normalize(text)[0]
