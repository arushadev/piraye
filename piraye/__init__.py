"""This module includes Normalizer and NormalizerBuilder"""
from .tasks.normalizer.normalizer import Normalizer
from .tasks.normalizer.multi_lingual_normalizer import MultiLingualNormalizer
from .tasks.normalizer.multi_lingual_normalizer_builder import MultiLingualNormalizerBuilder
from .tasks.normalizer.normalizer_builder import NormalizerBuilder
from .tasks.tokenizer.nltk_tokenizer import NltkSentenceTokenizer, NltkWordTokenizer
from .tasks.tokenizer.spacy_tokenizer import SpacySentenceTokenizer, SpacyWordTokenizer
from .tasks.tokenizer.base_tokenizer import Tokenizer
from .tasks.tokenizer.regex_tokenizer import URLTokenizer
from .tasks.tokenizer.paragraph_tokenizer import ParagraphTokenizer
