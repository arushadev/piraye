"""
Tokenizer module providing various tokenization strategies and pre-configured pipelines.

This module exports individual impl and pre-built tokenizer pipelines
for common text processing tasks.
"""

from .pipeline import TokenizerPipeline
from .impl.email_tokenizer import EmailTokenizer
from .impl.url_tokenizer import URLTokenizer
from .impl.html_tokenizer import HTMLTokenizer
from .impl.nltk_tokenizer import NltkSentenceTokenizer, NltkWordTokenizer
from .impl.paragraph_tokenizer import ParagraphTokenizer

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
