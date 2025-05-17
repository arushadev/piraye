import pytest
from ..piraye.tasks.tokenizer.nltk_tokenizer import NltkSentenceTokenizer
from ..piraye.tasks.tokenizer.regex_tokenizer import URLTokenizer
from ..piraye.tasks.tokenizer.paragraph_tokenizer import ParagraphTokenizer


@pytest.fixture
def sentence_tokenizer():
    return NltkSentenceTokenizer()


@pytest.fixture
def url_tokenizer():
    return URLTokenizer()


@pytest.fixture
def paragraph_tokenizer():
    return ParagraphTokenizer()


def test_merge_sentence_and_url(sentence_tokenizer, url_tokenizer):
    text = "Visit https://example.com. This is a test."
    url_tokens = url_tokenizer.tokenize(text)
    result = sentence_tokenizer.merge(text, url_tokens)
    assert len(result) > 0
    assert any("https://example.com" in token.content for token in result)


def test_merge_paragraph_and_url(paragraph_tokenizer, url_tokenizer):
    text = "Paragraph 1.\nhttps://example.com\nParagraph 2."
    url_tokens = url_tokenizer.tokenize(text)
    result = paragraph_tokenizer.merge(text, url_tokens)
    assert len(result) > 0
    assert any("https://example.com" in token.content for token in result)


def test_merge_sentence_and_paragraph(sentence_tokenizer, paragraph_tokenizer):
    text = "This is a sentence.\nThis is a paragraph."
    paragraph_tokens = paragraph_tokenizer.tokenize(text)
    result = sentence_tokenizer.merge(text, paragraph_tokens)
    assert len(result) > 0
    assert any("This is a sentence." in token.content for token in result)
    assert any("This is a paragraph." in token.content for token in result)