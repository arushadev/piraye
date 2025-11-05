# Test HTML tokenizer
# pylint: skip-file
from ..piraye import HTMLTokenizer


def test_html_tokenizer_object():
    """Test that HTMLTokenizer can be instantiated."""
    tokenizer = HTMLTokenizer()
    assert tokenizer is not None


def test_html_tokenizer_simple_tags():
    """Test extraction of simple HTML tags."""
    text = "This is <b>bold</b> and <i>italic</i> text."
    tokenizer = HTMLTokenizer()
    tokens = tokenizer.tokenize(text)
    assert len(tokens) == 4
    assert tokens[0].content == "<b>"
    assert tokens[1].content == "</b>"
    assert tokens[2].content == "<i>"
    assert tokens[3].content == "</i>"


def test_html_tokenizer_self_closing():
    """Test extraction of self-closing HTML tags."""
    text = "Line break here <br/> and image <img src='test.png'/>"
    tokenizer = HTMLTokenizer()
    tokens = tokenizer.tokenize(text)
    assert len(tokens) == 2
    assert tokens[0].content == "<br/>"
    assert tokens[1].content == "<img src='test.png'/>"


def test_html_tokenizer_with_attributes():
    """Test extraction of HTML tags with attributes."""
    text = '<a href="https://example.com" class="link">Click here</a>'
    tokenizer = HTMLTokenizer()
    tokens = tokenizer.tokenize(text)
    assert len(tokens) == 2
    assert tokens[0].content == '<a href="https://example.com" class="link">'
    assert tokens[1].content == "</a>"


def test_html_tokenizer_comments():
    """Test extraction of HTML comments."""
    text = "<!-- This is a comment --> <p>Paragraph</p>"
    tokenizer = HTMLTokenizer()
    tokens = tokenizer.tokenize(text)
    assert len(tokens) == 3
    assert tokens[0].content == "<!-- This is a comment -->"
    assert tokens[1].content == "<p>"
    assert tokens[2].content == "</p>"


def test_html_tokenizer_mixed_content():
    """Test extraction of HTML tags from mixed content."""
    text = "<html><head><title>Test</title></head><body><h1>Hello World</h1><p>This is a test.</p></body></html>"
    tokenizer = HTMLTokenizer()
    tokens = tokenizer.tokenize(text)
    assert len(tokens) == 12  # All opening and closing tags (6 pairs)


def test_html_tokenizer_no_tags():
    """Test that plain text without HTML returns no tokens."""
    text = "This is plain text without any HTML tags."
    tokenizer = HTMLTokenizer()
    tokens = tokenizer.tokenize(text)
    assert len(tokens) == 0


def test_html_tokenizer_position():
    """Test that token positions are correct."""
    text = "Text before <p>paragraph</p> text after"
    tokenizer = HTMLTokenizer()
    tokens = tokenizer.tokenize(text)
    assert len(tokens) == 2
    assert tokens[0].position == (12, 15)  # <p>
    assert tokens[1].position == (24, 28)  # </p>

