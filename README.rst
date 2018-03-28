Python Vietnamese Toolkit
=========================

Pyvi performs tokenizing / pos-tagging for Vietnamese in Python.  

Algorithm: Conditional Random Field

Vietnamese tokenizer f1_score = 0.978637686

Vietnamese pos tagging f1_score = 0.92520656

POS TAGS: 

- A - Adjective
- C - Coordinating conjunction
- E - Preposition
- I - Interjection
- L - Determiner
- M - Numeral
- N - Common noun
- Nc - Noun Classifier
- Ny - Noun abbreviation
- Np - Proper noun
- Nu - Unit noun
- P - Pronoun
- R - Adverb
- S -  Subordinating conjunction
- T - Auxiliary, modal words
- V - Verb
- X - Unknown
- F - Filtered out (punctuation)

============
Installation
============

At the command line with pip

.. code-block:: shell

    $ pip install pyvi

**Uninstall**

.. code-block:: shell

    $ pip uninstall pyvi

=====
Usage
=====

.. code-block:: python

    from pyvi import ViTokenizer, ViPosTagger

    ViTokenizer.tokenize(u"Trường đại học bách khoa hà nội")

    ViPosTagger.postagging(ViTokenizer.tokenize(u"Trường đại học Bách Khoa Hà Nội")




