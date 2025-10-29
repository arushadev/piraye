import pytest
from ..piraye.tasks.tokenizer import NltkSentenceTokenizer, ParagraphTokenizer, SpacySentenceTokenizer, \
    URLTokenizer, TokenizerPipeline


@pytest.fixture
def sentence_tokenizer():
    return NltkSentenceTokenizer()


@pytest.fixture
def url_tokenizer():
    return URLTokenizer()


@pytest.fixture
def paragraph_tokenizer():
    return ParagraphTokenizer()


def test_pipeline():
    pipeline = TokenizerPipeline([
        SpacySentenceTokenizer(),
        URLTokenizer()
    ])

    text = "Contact us at support@arusha.dev or info@piraye.ai."
    tokens = pipeline(text)
    print([t.content for t in tokens])

    assert len(tokens) == 1
    assert any("Contact us at support@arusha.dev or info@piraye.ai." in t.content for t in tokens)


def test_merge_sentence_and_url(sentence_tokenizer, url_tokenizer):
    text = "Visit https://example.com. This is a test."
    url_tokens = url_tokenizer.tokenize(text)
    result = sentence_tokenizer.merge(text, url_tokens)
    print(result)
    assert len(result) > 0
    assert any("https://example.com" in token.content for token in result)


def test_merge_paragraph_and_url(paragraph_tokenizer, url_tokenizer):
    text = "Paragraph 1.\nhttps://example.com\nParagraph 2."
    url_tokens = url_tokenizer.tokenize(text)
    result = paragraph_tokenizer.merge(text, url_tokens)
    for token in result:
        print(token)
    assert len(result) > 0
    assert any("https://example.com" in token.content for token in result)


def test_merge_sentence_and_paragraph(sentence_tokenizer, paragraph_tokenizer):
    text = "This is a sentence.\nThis is a paragraph."
    paragraph_tokens = paragraph_tokenizer.tokenize(text)
    result = sentence_tokenizer.merge(text, paragraph_tokens)
    print([token for token in result])

    assert len(result) > 0
    assert any("This is a sentence." in token.content for token in result)
    assert any("This is a paragraph." in token.content for token in result)
