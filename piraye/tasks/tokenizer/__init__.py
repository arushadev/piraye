# --- Custom pipelines ---

from .pipeline import TokenizerPipeline
from .tokenizers.regex_tokenizer import EmailTokenizer, URLTokenizer
from .tokenizers.nltk_tokenizer import NltkSentenceTokenizer, NltkWordTokenizer
from .tokenizers.paragraph_tokenizer import ParagraphTokenizer

paragraph_tokenizer_pipeline = TokenizerPipeline(
    [EmailTokenizer(), URLTokenizer(), NltkSentenceTokenizer(), ParagraphTokenizer()])
sentence_tokenizer_pipeline = TokenizerPipeline([EmailTokenizer(), URLTokenizer(), NltkSentenceTokenizer()])
word_tokenizer_pipeline = TokenizerPipeline([EmailTokenizer(), URLTokenizer(), NltkWordTokenizer()])

__all__ = [
    "paragraph_tokenizer_pipeline", "sentence_tokenizer_pipeline", "word_tokenizer_pipeline",
]
