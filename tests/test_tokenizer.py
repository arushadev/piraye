# testing Fibonacci number function
# pylint: skip-file

from ..piraye import NltkTokenizer


def test_object():
    tokenizer = NltkTokenizer()
    assert tokenizer is not None


def test_sample():
    text = "برای تست شماره ۲.۱ نوشته شده است"
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 7


def test_double_quotes():
    text = "'\"\"تست\""
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 5


def test_sentence_tokenizer():
    text = "sentence1 sad. \n asd asd \n asdasd \n sentence 2."
    tokenizer = NltkTokenizer()
    assert len(tokenizer.sentence_tokenize(text)) == 2
    assert len(tokenizer.sentence_span_tokenize(text)) == 2


def test_double_quotes2():
    text = "«»"
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 2
