import sys
import os
import string
import pickle

class ViPosTagger:
    filtered_tags = set(string.punctuation)
    filtered_tags.add(u'\u2026')
    filtered_tags.add(u'\u201d')
    filtered_tags.add(u'\u201c')
    filtered_tags.add(u'\u2019')
    filtered_tags.add('...')
    model_file = 'models/pyvipos.pkl'
    if sys.version_info[0] == 3:
        model_file = 'models/pyvipos3.pkl'

    with open(os.path.join(os.path.dirname(__file__), model_file), 'rb') as fin:
        model = pickle.load(fin)

    @staticmethod
    def word2features(sent, i, is_training):
        word = sent[i][0] if is_training else sent[i]

        features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            # 'word.isupper()': word.isupper(),
            'word.istitle()': word.istitle(),
            'word.isdigit()': word.isdigit(),
            'word[:1].isdigit()': word[:1].isdigit(),
            'word[:3].isupper()': word[:3].isupper(),
            #       'word.indict()': word in vi_words,
            'word.isfiltered': word in ViPosTagger.filtered_tags,
        }
        if i > 0:
            word1 = sent[i - 1][0] if is_training else sent[i - 1]
            features.update({
                '-1:word.lower()': word1.lower(),
                '-1:word.istitle()': word1.istitle(),
                '-1:word[:1].isdigit()': word1[:1].isdigit(),
                '-1:word[:3].isupper()': word1[:3].isupper(),
            })
            if i > 1:
                word2 = sent[i - 2][0] if is_training else sent[i - 2]
                features.update({
                    '-2:word.lower()': word2.lower(),
                    '-2:word.istitle()': word2.istitle(),
                    '-2:word.isupper()': word2.isupper(),
                })
        else:
            features['BOS'] = True

        if i < len(sent) - 1:
            word1 = sent[i + 1][0] if is_training else sent[i + 1]
            features.update({
                '+1:word.lower()': word1.lower(),
                '+1:word.istitle()': word1.istitle(),
                '+1:word[:1].isdigit()': word1[:1].isdigit(),
                '+1:word.isupper()': word1.isupper(),
            })
            if i < len(sent) - 2:
                word2 = sent[i + 2][0] if is_training else sent[i + 2]
                features.update({
                    '+2:word.lower()': word2.lower(),
                    '+2:word.istitle()': word2.istitle(),
                    '+2:word.isupper()': word2.isupper(),
                })
        else:
            features['EOS'] = True

        return features

    @staticmethod
    def sent2features(sent, is_training):
        return [ViPosTagger.word2features(sent, i, is_training) for i in range(len(sent))]

    @staticmethod
    def postagging(str):
        return ViPosTagger.postagging_tokens(str.split(' '))

    @staticmethod
    def postagging_tokens(tokens):
        labels = ViPosTagger.model.predict([ViPosTagger.sent2features(tokens, False)])
        # for i in range(len(labels[0])):
        #    print tmp[i], labels[0][i]
        return tokens, labels[0]


def postagging(str):
    return ViPosTagger.postagging(str)


def postagging_tokens(tokens):
    return ViPosTagger.postagging_tokens(tokens)
