# testing Fibonacci number function
# pylint: skip-file
from ..piraye import NltkTokenizer, SpacyTokenizer


def test_object():
    tokenizer = NltkTokenizer()
    assert tokenizer is not None


def test_sample():
    text = "برای تست شماره ۲.۱ نوشته شده است"
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 7


def test_sample_spacy():
    text = "برای تست (شماره ۲.۱ نوشته) شده است"
    tokenizer = SpacyTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 9


def test_double_quotes():
    text = "'\"\"تست\""
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 5


def test_sentence_tokenizer():
    text = "sentence1 sad. \n asd asd \n asdasd \n sentence 2."
    tokenizer = NltkTokenizer()
    assert len(tokenizer.sentence_tokenize(text)) == 2
    assert len(tokenizer.sentence_span_tokenize(text)) == 2


def test_paragraph_tokenizer():
    text = "par1 sen1 sad.  par1 \n sen2. par1 \n\n sen3.\n par2 sen1.\n\n\n\n   par3 sen1. \n par4 sen1.\n\n"
    tokenizer = NltkTokenizer()
    assert len(tokenizer.paragraph_tokenize(text)) == 4
    assert len(tokenizer.paragraph_span_tokenize(text)) == 4
    assert len(tokenizer.paragraph_tokenize("par1 sen1 sad.")) == 1
    assert len(tokenizer.paragraph_tokenize("par1 sen1 sad. par1 \n sen2. ")) == 1


def test_paragraph_tokenizer_spacy():
    text = "par1 sen1 sad.  par1 \n sen2. par1 \n\n sen3.\n par2 sen1.\n\n\n\n   par3 sen1. \n par4 sen1.\n\n"
    tokenizer = SpacyTokenizer()
    assert len(tokenizer.paragraph_tokenize(text)) == 4
    assert len(tokenizer.paragraph_span_tokenize(text)) == 4
    assert len(tokenizer.paragraph_tokenize("par1 sen1 sad.")) == 1
    assert len(tokenizer.paragraph_tokenize("par1 sen1 sad. par1 \n sen2. ")) == 1


def test_sentence_tokenizer_spacy():
    text = "sentence1 sad. \n asd asd \n asdasd \n sentence 2."
    tokenizer = SpacyTokenizer()
    assert len(tokenizer.sentence_tokenize(text)) == 2
    assert len(tokenizer.sentence_span_tokenize(text)) == 2


def test_double_quotes2():
    text = "«»"
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 2


def test_link():
    # To check nltk is functioning wrong for links
    text = "این یک لینک تست است https://www.google.com "
    tokenizer = NltkTokenizer()
    assert len(tokenizer.word_tokenize(text)) != 9


def test_link_spacy():
    text = "این یک لینک، (تست) است https://www.google.com "
    tokenizer = SpacyTokenizer()
    assert len(tokenizer.word_tokenize(text)) == 9
