# pyvi
Python Vietnamese Toolkit

This tool makes it easy to do tokenizing / pos-tagging Vietnamese with Python.

Algorithm: Conditional Random Field Vietnamese tokenizer f1_score = 0.978637686 Vietnamese pos tagging f1_score = 0.92520656

POS TAGS: A - Adjective C - Coordinating conjunction E - Preposition I - Interjection L - Determiner M - Numeral N - Common noun Nc - Noun Classifier Ny - Noun abbreviation Np - Proper noun Nu - Unit noun P - Pronoun R - Adverb S - Subordinating conjunction T - Auxiliary, modal words V - Verb X - Unknown F - Filtered out (punctuation)

# Installation

At the command line with pip
```
pip install pyvi
```

# Uninstall

```
pip uninstall pyvi
```

# Usage

```
>>> from pyvi.pyvi import ViTokenizer, ViPosTagger
'Trường đại_học bách_khoa hà_nội'
>>> ViTokenizer.tokenize(u"Trường đại học bách khoa hà nội")
>>> ViPosTagger.postagging(ViTokenizer.tokenize(u"Trường đại học Bách Khoa Hà Nội"))
(['Trường', 'đại_học', 'Bách_Khoa', 'Hà_Nội'], ['N', 'N', 'Np', 'Np'])
```
