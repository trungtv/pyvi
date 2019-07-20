__author__ = 'trungtv'
import string
import pickle
from sklearn_crfsuite import CRF
import gc
import sys
import os 
gc.collect()

class ViDiac:

    class FeatureGenerator:
        def __init__(self, tokens):
            self.tokens = tokens

        def gen_inner_windows(self, index):
            mention_text = self.tokens[index]
            yield ('current_char_{}', mention_text.lower())
            yield ('is_digit_', (mention_text.isdigit()))
            yield ('is_punc_', (mention_text in string.punctuation))
            left_index = index
            while left_index > 0 and self.tokens[left_index] != ' ':
                left_index -= 1
                yield '{}_char_'.format(left_index - index), self.tokens[left_index]
                yield '{}_isdigit_'.format(left_index - index), self.tokens[left_index].isdigit()
                yield '{}_ispunct_'.format(left_index - index), self.tokens[left_index] in string.punctuation

            right_index = index
            while right_index < len(self.tokens) - 1 and self.tokens[right_index] != ' ':
                right_index += 1
                yield '{}_char_'.format(right_index - index), self.tokens[right_index]
                yield '{}_isdigit_'.format(right_index - index), self.tokens[right_index].isdigit()
                yield '{}_ispunct_'.format(right_index - index), self.tokens[right_index] in string.punctuation

            if left_index != right_index:
                yield ('inner_word_', ''.join(self.tokens[left_index:right_index]))

        def gen_left_windows(self, index, MAX_SPACE):
            num_words = 0
            last_space_index = index
            left_index = index
            while num_words < MAX_SPACE and left_index > 0:
                left_index -= 1
                if self.tokens[left_index] == ' ' or left_index == 0:
                    num_words += 1
                    if num_words == 1:
                        last_space_index = left_index
                    else:
                        yield '{}_word_'.format(1 - num_words), ''.join(self.tokens[left_index + 1:last_space_index])
                        last_space_index = left_index
                if self.tokens[left_index] in '.!?':
                    break

                    # yield '{}_char_'.format(left_index - index), self.tokens[left_index]
                    # yield '{}_isdigit_'.format(left_index - index), self.tokens[left_index].isdigit()
                    # yield '{}_ispunct_'.format(left_index - index), self.tokens[left_index] in string.punctuation

        def gen_right_windows(self, index, MAX_SPACE):
            num_words = 0
            last_space_index = index
            right_index = index
            while num_words < MAX_SPACE and right_index < len(self.tokens) - 1:
                right_index += 1

                if self.tokens[right_index] == ' ' or right_index == len(self.tokens):
                    num_words += 1
                    if num_words == 1:
                        last_space_index = right_index
                    else:
                        yield '{}_word_'.format(num_words - 1), ''.join(self.tokens[last_space_index + 1: right_index])
                        last_space_index = right_index
                if self.tokens[right_index] in '.!?':
                    break

                    # yield '{}_char_'.format(right_index - index), self.tokens[right_index]
                    # yield '{}_isdigit_'.format(right_index - index), self.tokens[right_index].isdigit()
                    # yield '{}_ispunct_'.format(right_index - index), self.tokens[right_index] in string.punctuation

    maAciiTexlex = [7845, 7847, 7849, 7851, 7853, 226, 225, 224, 7843, 227, 7841, 7855, 7857, 7859, \
                    7861, 7863, 259, 250, 249, 7911, 361, 7909, 7913, 7915, 7917, 7919, 7921, 432, \
                    7871, 7873, 7875, 7877, 7879, 234, 233, 232, 7867, 7869, 7865, 7889, 7891, 7893, \
                    7895, 7897, 244, 243, 242, 7887, 245, 7885, 7899, 7901, 7903, 7905, 7907, 417, \
                    237, 236, 7881, 297, 7883, 253, 7923, 7927, 7929, 7925, 273, 7844, 7846, 7848, \
                    7850, 7852, 194, 193, 192, 7842, 195, 7840, 7854, 7856, 7858, 7860, 7862, 258, \
                    218, 217, 7910, 360, 7908, 7912, 7914, 7916, 7918, 7920, 431, 7870, 7872, 7874, \
                    7876, 7878, 202, 201, 200, 7866, 7868, 7864, 7888, 7890, 7892, 7894, 7896, 212, \
                    211, 210, 7886, 213, 7884, 7898, 7900, 7902, 7904, 7906, 416, 205, 204, 7880, 296, \
                    7882, 221, 7922, 7926, 7928, 7924, 272]
    telex = ["aas", "aaf", "aar", "aax", "aaj", "aa", "as", "af", "ar", "ax", "aj", "aws", "awf", \
             "awr", "awx", "awj", "aw", "us", "uf", "ur", "ux", "uj", "uws", "uwf", "uwr", "uwx", \
             "uwj", "uw", "ees", "eef", "eer", "eex", "eej", "ee", "es", "ef", "er", "ex", "ej", \
             "oos", "oof", "oor", "oox", "ooj", "oo", "os", "of", "or", "ox", "oj", "ows", "owf", \
             "owr", "owx", "owj", "ow", "is", "if", "ir", "ix", "ij", "ys", "yf", "yr", "yx", "yj", \
             "dd", "AAS", "AAF", "AAR", "AAX", "AAJ", "AA", "AS", "AF", "AR", "AX", \
             "AJ", "AWS", "AWF", "AWR", "AWX", "AWJ", "AW", "US", "UF", "UR", "UX", \
             "UJ", "UWS", "UWF", "UWR", "UWX", "UWJ", "UW", "EES", "EEF", "EER", \
             "EEX", "EEJ", "EE", "ES", "EF", "ER", "EX", "EJ", "OOS", "OOF", "OOR", \
             "OOX", "OOJ", "OO", "OS", "OF", "OR", "OX", "OJ", "OWS", "OWF", "OWR", \
             "OWX", "OWJ", "OW", "IS", "IF", "IR", "IX", "IJ", "YS", "YF", "YR", "YX", \
             "YJ", "DD"]

    mapping = {}
    reversed_mapping = {}

    if sys.version_info[0] == 3:
        for i in range(len(telex)):
            mapping[chr(maAciiTexlex[i])] = telex[i]
            reversed_mapping[telex[i]] = chr(maAciiTexlex[i])
    else:
        for i in range(len(telex)):
            mapping[unichr(maAciiTexlex[i])] = telex[i]
            reversed_mapping[telex[i]] = unichr(maAciiTexlex[i])
    reversed_mapping

    crf = CRF(model_filename=os.path.join(os.path.dirname(__file__), 'models/vidiac.crfsuite'))
    data = pickle.dumps(crf, protocol=pickle.HIGHEST_PROTOCOL)
    model = pickle.loads(data)

    @staticmethod
    def prepare_data(str_line):
        tokens = []
        labels = []
        for ch in str_line:
            label = ''
            if ch.isupper():
                label += 'U'
            else:
                label += 'L'

            if ch not in ViDiac.mapping:
                # yield "{}\t{}".format(ch.lower(), label)
                # yield (ch.lower(), label)
                tokens.append(ch.lower())
                labels.append(label)
            else:
                ch = ch.lower()
                chmap = ViDiac.mapping[ch]
                if chmap[0] == chmap[1]:
                    label += 'm'
                elif chmap[1] == 'w':
                    label += 'w'
                if chmap[-1] in 'sfrxj':
                    label += chmap[-1]
                # yield "{}\t{}".format(chmap[0], label)
                # yield (chmap[0], label)
                tokens.append(chmap[0])
                labels.append(label)
        return tokens, labels

    @staticmethod
    def word2features(i, feature_generator):

        features = {
            'bias': 1.0,
        }

        for (key, value) in feature_generator.gen_inner_windows(i):
            features[key] = value
        for (key, value) in feature_generator.gen_left_windows(i, 2):
            features[key] = value
        for (key, value) in feature_generator.gen_right_windows(i, 2):
            features[key] = value
        return features

    @staticmethod
    def sent2features(tokens):
        feature_generator = ViDiac.FeatureGenerator(tokens)
        return [ViDiac.word2features(i, feature_generator) for i in range(len(tokens))]

    @staticmethod
    def doit(str_sentence):
        list_char = list(str_sentence.lower())
        labels = ViDiac.model.predict([ViDiac.sent2features(list_char)])
        # output = tmp[0]
        # print labels[0]
        output = u''
        for i in range(len(list_char)):
            # print list_char[i], labels[0][i]
            if labels[0][i] == 'L':
                output += list_char[i]
            elif labels[0][i] == 'U':
                output += list_char[i].upper()
            else:
                # print "label_{}".format(labels[0][i])
                upcase = False
                unichar = list_char[i]
                for label in labels[0][i]:
                    if label == 'U':
                        upcase = True
                    elif label == 'L':
                        continue
                    elif label == 'm':
                        unichar += unichar
                    else:
                        unichar += label
                if upcase:
                    unichar = unichar.upper()
                # print unichar
                output += ViDiac.reversed_mapping[unichar]
        return output

def add_accents(s):
    return ViDiac.doit(s)
