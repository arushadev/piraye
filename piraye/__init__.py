"""This module includes Normalizer and NormalizerBuilder"""
from .tasks.normalizer.normalizer import Normalizer
from .tasks.normalizer.multi_lingual_normalizer import MultiLingualNormalizer
from .tasks.normalizer.multi_lingual_normalizer_builder import MultiLingualNormalizerBuilder
from .tasks.normalizer.normalizer_builder import NormalizerBuilder
from .tasks.tokenizer.tokenizers.nltk_tokenizer import NltkSentenceTokenizer, NltkWordTokenizer
from .tasks.tokenizer.tokenizers.spacy_tokenizer import SpacySentenceTokenizer, SpacyWordTokenizer
from .tasks.tokenizer.tokenizers.base_tokenizer import Tokenizer
from .tasks.tokenizer.tokenizers.regex_tokenizer import URLTokenizer
from .tasks.tokenizer.tokenizers.paragraph_tokenizer import ParagraphTokenizer
