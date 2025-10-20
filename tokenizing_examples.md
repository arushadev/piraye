## ⚙️ Tokenizer Pipeline Example (Sentence & paragraph)
 
```python
from piraye.tasks.tokenizer.nltk_tokenizer import NltkSentenceTokenizer
from piraye.tasks.tokenizer.paragraph_tokenizer import ParagraphTokenizer 
from piraye.tasks.tokenizer.pipeline import TokenizerPipeline

pipeline = TokenizerPipeline([
    NltkSentenceTokenizer(),
    ParagraphTokenizer()
])

text = "This is a sentence.\nThis is a paragraph."
tokens = pipeline(text)
print([token for token in tokens])

# [Token(content='This is a sentence.', type='Paragraph', position=(0, 19), sub_tokens=[Token(content='This is a sentence.', type='NltkSentenceTokenizer', position=(0, 19), sub_tokens=[])]), 
#  Token(content='\nThis is a paragraph.', type='Paragraph', position=(19, 40), sub_tokens=[Token(content='This is a paragraph.', type='NltkSentenceTokenizer', position=(20, 40), sub_tokens=[])])]
```
## ⚙️ Spacy Sentence Tokenizer Example

```python
from piraye.tasks.tokenizer.spacy_tokenizer import SpacySentenceTokenizer

text = "Piraye is powerful. It supports Persian and English."
tokenizer = SpacySentenceTokenizer()
tokens = tokenizer.tokenize(text)
for token in tokens:
    print(token)

# Token(type=SpacySentenceTokenizer, content='Piraye is powerful.', position=(0, 19), sub_tokens=0)
# Token(type=SpacySentenceTokenizer, content=' It supports Persian and English.', position=(19, 52), sub_tokens=0)
```
## ⚙️ Spacy Word Tokenizer Example

```python
from piraye.tasks.tokenizer.spacy_tokenizer import SpacyWordTokenizer

text = "Piraye is a multilingual NLP toolkit."
tokenizer = SpacyWordTokenizer()
tokens = tokenizer.tokenize(text)
for token in tokens:
    print(token)

# Token(type=SpacyWordTokenizer, content='is ', position=(7, 10), sub_tokens=0)
# Token(type=SpacyWordTokenizer, content='a ', position=(10, 12), sub_tokens=0)
# Token(type=SpacyWordTokenizer, content='multilingual ', position=(12, 25), sub_tokens=0)
# Token(type=SpacyWordTokenizer, content='NLP ', position=(25, 29), sub_tokens=0)
# Token(type=SpacyWordTokenizer, content='toolkit.', position=(29, 37), sub_tokens=0)
# Token(type=SpacyWordTokenizer, content='.', position=(36, 38), sub_tokens=0)
```

## ⚙️ Email Tokenizer Example

```python
from piraye.tasks.tokenizer.regex_tokenizer import EmailTokenizer

text = "Contact us at support@arusha.dev or info@piraye.ai."
tokens = EmailTokenizer().tokenize(text)
for token in tokens:
    print(token)
    
# Token(type=EmailTokenizer, content='support@arusha.dev', position=(14, 32), sub_tokens=0)
# Token(type=EmailTokenizer, content='info@piraye.ai', position=(36, 50), sub_tokens=0)
```

## ⚙️ URL Tokenizer Example

```python
from piraye.tasks.tokenizer.regex_tokenizer import URLTokenizer

text = "Visit https://www.arusha.dev or follow our GitHub at https://github.com/arushadev"
tokens = URLTokenizer().tokenize(text)
for token in tokens:
    print(token)

# Token(type=URLTokenizer, content='https://www.arusha.dev', position=(6, 28), sub_tokens=0)
# Token(type=URLTokenizer, content='https://github.com/arushadev', position=(53, 81), sub_tokens=0)
```
