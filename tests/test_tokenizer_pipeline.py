import pytest
from ..piraye.tasks.tokenizer.pipeline import TokenizerPipeline
from ..piraye.tasks.tokenizer.paragraph_tokenizer import ParagraphTokenizer
from ..piraye.tasks.tokenizer.regex_tokenizer import URLTokenizer, EmailTokenizer
from ..piraye.tasks.tokenizer.base_tokenizer import Tokenizer
from ..piraye.tasks.tokenizer.token import Token

# Add import for pre-defined pipelines
from ..piraye.tasks.tokenizer import (
    paragraph_tokenizer_pipeline,
    sentence_tokenizer_pipeline,
    word_tokenizer_pipeline,
)

class DummyCharTokenizer(Tokenizer):
    def tokenize(self, text):
        return [
            Token(content=c, position=(i, i+1), type="Char", sub_tokens=[])
            for i, c in enumerate(text) if c.strip()
        ]

@pytest.fixture
def sample_text():
    return (
        "Hello world!\n"
        "Contact us at test@example.com or visit https://example.com.\n"
        "Another paragraph."
    )

def test_empty_pipeline(sample_text):
    pipeline = TokenizerPipeline([])
    assert pipeline(sample_text) == []

def test_single_paragraph_tokenizer(sample_text):
    pipeline = TokenizerPipeline([ParagraphTokenizer()])
    tokens = pipeline(sample_text)
    assert len(tokens) == 3
    assert all(t.type == "Paragraph" for t in tokens)
    assert tokens[0].content.startswith("Hello world!")

def test_single_url_tokenizer():
    text = "Check this: https://foo.com and http://bar.com"
    pipeline = TokenizerPipeline([URLTokenizer()])
    tokens = pipeline(text)
    urls = [t.content for t in tokens]
    assert "https://foo.com" in urls
    assert "http://bar.com" in urls
    assert all(t.type == "URLTokenizer" for t in tokens)

def test_single_email_tokenizer():
    text = "Emails: a@b.com, x.y@z.org"
    pipeline = TokenizerPipeline([EmailTokenizer()])
    tokens = pipeline(text)
    emails = [t.content for t in tokens]
    assert "a@b.com" in emails
    assert "x.y@z.org" in emails
    assert all(t.type == "EmailTokenizer" for t in tokens)

def test_chain_paragraph_and_url_tokenizer(sample_text):
    pipeline = TokenizerPipeline([ParagraphTokenizer(), URLTokenizer()])
    tokens = pipeline(sample_text)
    # Should merge paragraph tokens with URL tokens
    assert any("https://example.com" in t.content or any("https://example.com" in st.content for st in t.sub_tokens) for t in tokens)
    assert any(t.type == "Paragraph" for t in tokens)

def test_chain_url_and_email_tokenizer():
    text = "Contact: foo@bar.com and https://bar.com"
    pipeline = TokenizerPipeline([URLTokenizer(), EmailTokenizer()])
    tokens = pipeline(text)
    # Should merge URL and Email tokens
    assert any("foo@bar.com" in t.content or any("foo@bar.com" in st.content for st in t.sub_tokens) for t in tokens)
    assert any("https://bar.com" in t.content or any("https://bar.com" in st.content for st in t.sub_tokens) for t in tokens)

def test_chain_paragraph_and_char_tokenizer(sample_text):
    pipeline = TokenizerPipeline([ParagraphTokenizer(), DummyCharTokenizer()])
    tokens = pipeline(sample_text)
    # Each paragraph token should have sub_tokens for each character
    assert all(any(len(st.content) == 1 for st in t.sub_tokens) for t in tokens)

def test_merging_preserves_positions(sample_text):
    pipeline = TokenizerPipeline([ParagraphTokenizer(), DummyCharTokenizer()])
    tokens = pipeline(sample_text)
    for t in tokens:
        for st in t.sub_tokens:
            assert t.position[0] <= st.position[0] < st.position[1] <= t.position[1]

def test_predefined_paragraph_tokenizer_pipeline(sample_text):
    tokens = paragraph_tokenizer_pipeline(sample_text)
    # Should return paragraph tokens, each with sub_tokens for sentence and URL/email
    assert len(tokens) == 3
    assert all(t.type == "Paragraph" for t in tokens)
    # Check that at least one sub_token is a sentence or URL/email
    assert any(
        any(st.type in ("NltkSentenceTokenizer", "URLTokenizer", "EmailTokenizer") for st in t.sub_tokens)
        for t in tokens
    )

def test_predefined_sentence_tokenizer_pipeline(sample_text):
    tokens = sentence_tokenizer_pipeline(sample_text)
    # Should return sentence tokens, each with sub_tokens for URL/email
    assert any(t.type == "NltkSentenceTokenizer" for t in tokens)
    assert any(
        any(st.type in ("URLTokenizer", "EmailTokenizer") for st in t.sub_tokens)
        for t in tokens
    )

def test_predefined_word_tokenizer_pipeline(sample_text):
    tokens = word_tokenizer_pipeline(sample_text)
    # Should return word tokens, each with sub_tokens for URL/email
    assert any(t.type == "NltkWordTokenizer" for t in tokens)
    assert any(
        any(st.type in ("URLTokenizer", "EmailTokenizer") for st in t.sub_tokens)
        for t in tokens
    )
