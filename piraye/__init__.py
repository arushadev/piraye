"""This module includes Normalizer and NormalizerBuilder"""
from .tasks.normalizer.normalizer import Normalizer
from .tasks.normalizer.multi_lingual_normalizer import MultiLingualNormalizer
from .tasks.normalizer.multi_lingual_normalizer_builder import MultiLingualNormalizerBuilder
from .tasks.normalizer.normalizer_builder import NormalizerBuilder
from .tasks.tokenizer import NltkSentenceTokenizer, NltkWordTokenizer
from .tasks.tokenizer import SpacySentenceTokenizer, SpacyWordTokenizer
from .tasks.tokenizer.tokenizers.base_tokenizer import Tokenizer
from .tasks.tokenizer import URLTokenizer, EmailTokenizer, HTMLTokenizer
from .tasks.tokenizer import ParagraphTokenizer
