# testing Fibonacci number function
# pylint: skip-file

from ..src import NltkTokenizer


def test_object():
    tokenizer = NltkTokenizer()
    assert tokenizer is not None


def test_sample():
    text = "برای تست شماره ۲.۱ نوشته شده است"
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 7


def test_double_quotes():
    text = "\"\"تست\""
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 4


def test_double_quotes2():
    text = "«»"
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 2
