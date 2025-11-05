import pytest
from ..piraye.tasks.tokenizer.token import Token
from ..piraye.tasks.tokenizer.tokenizers.base_tokenizer import Tokenizer
from ..piraye.tasks.tokenizer.pipeline import TokenizerPipeline


class DummyTokenizer(Tokenizer):
    def tokenize(self, text: str):
        # Dummy implementation for testing
        result = []
        start = 0
        for i, word in enumerate(text.split()):
            result.append(
                Token(content=text[start:start + len(word) + 1], position=(start, start + len(word) + 1), type="word",
                      sub_tokens=[]))
            start += len(word) + 1
        return result


class PreviousTokensTokenizer(Tokenizer):
    def tokenize(self, text: str):
        return [
            Token(content="This", position=(0, 4), type="word", sub_tokens=[]),
            Token(content="is", position=(5, 7), type="word", sub_tokens=[]),
        ]


class OverlappingTokensTokenizer(Tokenizer):
    def tokenize(self, text: str):
        return [
            Token(content="This", position=(0, 4), type="word", sub_tokens=[]),
            Token(content="is a", position=(5, 9), type="phrase", sub_tokens=[]),
        ]


class NestedTokensTokenizer(Tokenizer):
    def tokenize(self, text: str):
        return [
            Token(content="Nested", position=(0, 6), type="word", sub_tokens=[]),
            Token(content="tokens", position=(7, 13), type="word", sub_tokens=[]),
        ]


class EmptyPreviousTokensTokenizer(Tokenizer):
    def tokenize(self, text: str):
        return []


class ExistingTokenTokenizer(Tokenizer):
    def tokenize(self, text: str):
        return [
            Token(content="Existing", position=(0, 8), type="word", sub_tokens=[]),
        ]


@pytest.fixture
def tokenizer():
    return DummyTokenizer()


def test_merge_non_overlapping(tokenizer):
    text = "This is a test"
    pipeline = TokenizerPipeline([PreviousTokensTokenizer(), tokenizer])  # Added PreviousTokensTokenizer to the pipeline
    result = pipeline.tokenize(text)  # Use tokenize instead of merge
    print(result)
    assert len(result) == 4
    assert result[0].content == "This "
    assert result[1].content == "is "
    assert result[2].content == "a "
    assert result[3].content == "test"


def test_merge_overlapping(tokenizer):
    text = "This is a test"
    pipeline = TokenizerPipeline([OverlappingTokensTokenizer(), tokenizer])
    result = pipeline.tokenize(text)
    assert len(result) == 3
    assert result[1].content == "is a "
    assert result[2].content == "test"


def test_merge_nested_tokens(tokenizer):
    text = "Nested tokens example"
    pipeline = TokenizerPipeline([NestedTokensTokenizer(), tokenizer])
    result = pipeline.tokenize(text)
    assert len(result) == 3
    assert result[0].content == "Nested "
    assert result[1].content == "tokens "
    assert result[2].content == "example"


def test_merge_empty_previous_tokens(tokenizer):
    text = "Only new tokens"
    pipeline = TokenizerPipeline([EmptyPreviousTokensTokenizer(), tokenizer])
    result = pipeline.tokenize(text)
    assert len(result) == 3
    assert result[0].content == "Only "
    assert result[1].content == "new "
    assert result[2].content == "tokens"


def test_merge_empty_text(tokenizer):
    text = "Existing"
    pipeline = TokenizerPipeline([ExistingTokenTokenizer(), tokenizer])
    result = pipeline.tokenize(text)
    print(result)
    assert len(result) == 1
    assert result[0].content == "Existing"
