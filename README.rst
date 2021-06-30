Python Vietnamese Toolkit
=========================
What's New (0.1)
================
- Retrain a new tokenization model on a much bigger dataset. F1 score =0.985

- Add training data and training code

- Better integration to spacy.io (removing redundant spaces between tokens after tokenization. Eg. Việt Nam , 12 / 22 / 2020 => Việt Nam, 12/22/2020]

Functionality
=============

- Tokenization

- POS tagging

- Accents removal

- Accents adding


Algorithm: Conditional Random Field

Vietnamese tokenizer f1_score = 0.985

Vietnamese pos tagging f1_score = 0.925


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

    from pyvi import ViUtils
    ViUtils.remove_accents(u"Trường đại học bách khoa hà nội")

    from pyvi import ViUtils
    ViUtils.add_accents(u'truong dai hoc bach khoa ha noi')


