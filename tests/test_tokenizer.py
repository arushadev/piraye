# testing Fibonacci number function
# pylint: skip-file
from ..piraye import NltkWordTokenizer, SpacyWordTokenizer, ParagraphTokenizer, SpacySentenceTokenizer, \
    NltkSentenceTokenizer, URLTokenizer


def test_object():
    tokenizer = NltkWordTokenizer()
    assert tokenizer is not None


def test_sample():
    text = "برای تست شماره ۲.۱ نوشته شده است"
    tokenizer = NltkWordTokenizer()
    assert len(tokenizer.tokenize(text)) == 7


def test_sample_spacy():
    text = "برای تست (شماره ۲.۱ نوشته) شده است"
    tokenizer = SpacyWordTokenizer()
    assert len(tokenizer.tokenize(text)) == 9


def test_double_quotes():
    text = "'\"\"تست\""
    tokenizer = NltkWordTokenizer()
    assert len(tokenizer.tokenize(text)) == 5


def test_sentence_tokenizer():
    text = "sentence1 sad. \n asd asd \n asdasd \n sentence 2."
    tokenizer = NltkSentenceTokenizer()
    assert len(tokenizer.tokenize(text)) == 2
    assert len(tokenizer.tokenize(text)) == 2


def test_paragraph_tokenizer():
    text = "par1 sen1 sad.  par1 \n sen2. par1 \n\n sen3.\n par2 sen1.\n\n\n\n   par3 sen1. \n par4 sen1.\n\n"
    sent_tokenizer = NltkSentenceTokenizer()
    sentences = sent_tokenizer.tokenize(text)
    paragraph_tokenizer = ParagraphTokenizer()
    paragraphs = paragraph_tokenizer.merge(text, sentences)
    assert len(paragraphs) == 5


def test_paragraph_tokenizer_spacy():
    text = "par1 sen1 sad.  par1 \n sen2. par1 \n\n sen3.\n par2 sen1.\n\n\n\n   par3 sen1. \n par4 sen1.\n\n"
    sent_tokenizer = SpacySentenceTokenizer()
    sentences = sent_tokenizer.tokenize(text)
    paragraph_tokenizer = ParagraphTokenizer()
    paragraphs = paragraph_tokenizer.merge(text, sentences)
    assert len(paragraphs) == 5


def test_sentence_tokenizer_spacy():
    text = "sentence1 sad. \n asd asd \n asdasd \n sentence 2."
    tokenizer = SpacySentenceTokenizer()
    assert len(tokenizer.tokenize(text)) == 2


def test_double_quotes2():
    text = "«»"
    tokenizer = NltkWordTokenizer()
    assert len(tokenizer.tokenize(text)) == 2


def test_link():
    text = "این یک لینک تست است https://www.google.com "
    urls = URLTokenizer().tokenize(text)
    tokenizer = NltkWordTokenizer()
    assert len(tokenizer.merge(text, urls)) != 9


def test_link_spacy():
    text = "این یک لینک، (تست) است https://www.google.com "
    tokenizer = SpacyWordTokenizer()
    assert len(tokenizer.tokenize(text)) == 9
