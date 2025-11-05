"""
Tokenizer module providing various tokenization strategies and pre-configured pipelines.

This module exports individual tokenizers and pre-built tokenizer pipelines
for common text processing tasks.
"""

from .pipeline import TokenizerPipeline
from .tokenizers.regex_tokenizers import EmailTokenizer, URLTokenizer, HTMLTokenizer
from .tokenizers.nltk_tokenizer import NltkSentenceTokenizer, NltkWordTokenizer
from .tokenizers.paragraph_tokenizer import ParagraphTokenizer

# --- Pre-configured tokenizer pipelines ---

# Pipeline that tokenizes text into paragraphs, handling emails, URLs, and sentences
paragraph_tokenizer_pipeline = TokenizerPipeline([
    EmailTokenizer(),
    URLTokenizer(),
    NltkSentenceTokenizer(),
    ParagraphTokenizer()
])

# Pipeline that tokenizes text into sentences, handling emails and URLs
sentence_tokenizer_pipeline = TokenizerPipeline([
    EmailTokenizer(),
    URLTokenizer(),
    NltkSentenceTokenizer()
])

# Pipeline that tokenizes text into words, handling emails and URLs
word_tokenizer_pipeline = TokenizerPipeline([
    EmailTokenizer(),
    URLTokenizer(),
    NltkWordTokenizer()
])

__all__ = [
    # Pipelines
    "paragraph_tokenizer_pipeline",
    "sentence_tokenizer_pipeline",
    "word_tokenizer_pipeline",
    # Tokenizers
    "EmailTokenizer",
    "URLTokenizer",
    "HTMLTokenizer",
    "NltkSentenceTokenizer",
    "NltkWordTokenizer",
    "ParagraphTokenizer",
    # Pipeline class
    "TokenizerPipeline",
]
