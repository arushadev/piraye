import pytest

from ..piraye.tasks.tokenizer.nltk_tokenizer import NltkSentenceTokenizer
from ..piraye.tasks.tokenizer.paragraph_tokenizer import ParagraphTokenizer


@pytest.fixture
def paragraph_tokenizer():
    return ParagraphTokenizer()


def test_single_paragraph(paragraph_tokenizer):
    text = "This is a single paragraph."
    result = paragraph_tokenizer.tokenize(text)
    assert len(result) == 1
    assert result[0].content == "This is a single paragraph."
    assert result[0].position == (0, len(text))


def test_multiple_paragraphs(paragraph_tokenizer):
    text = "First paragraph.\nSecond paragraph.\nThird paragraph."
    result = paragraph_tokenizer.tokenize(text)
    print(result)
    assert len(result) == 3
    assert result[0].content == "First paragraph."
    assert result[0].position == (0, 16)
    assert result[1].content == "\nSecond paragraph."
    assert result[1].position == (16, 34)
    assert result[2].content == "\nThird paragraph."
    assert result[2].position == (34, len(text))


def test_empty_text(paragraph_tokenizer):
    text = ""
    result = paragraph_tokenizer.tokenize(text)
    assert len(result) == 0


def test_text_with_only_newlines(paragraph_tokenizer):
    text = "\n\n\n"
    result = paragraph_tokenizer.tokenize(text)
    assert len(result) == 1


def test_text_with_spaces_and_newlines(paragraph_tokenizer):
    text = "   \nFirst paragraph.\n   \nSecond paragraph.\n   "
    nltk_tokenizer = NltkSentenceTokenizer()
    # nltk_tokens = nltk_tokenizer.tokenize(text)
    # print(nltk_tokens)
    # print(paragraph_tokenizer.merge(text, nltk_tokens))
    result = paragraph_tokenizer.tokenize(text)
    assert len(result) == 3
    assert result[1].content == "\nFirst paragraph.\n   "
    assert result[1].position == (3, 24)
    assert result[2].content == "\nSecond paragraph.\n   "
    assert result[2].position == (24, len(text))
