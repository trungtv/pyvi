from unittest import TestCase
from pyvi.ViTokenizer import ViTokenizer

class TestViTokenizer(TestCase):
    def test_sylabelize(self):
        text = "Thủ tướng: Chỉ số thị trường chứng khoán Việt Nam trong top 3 thế giới"
        actual = ViTokenizer.sylabelize(text)
        expected = ['Thủ', 'tướng', ':', 'Chỉ', 'số', 'thị', 'trường', 'chứng', 'khoán', 'Việt', 'Nam', 'trong',
                        'top', '3', 'thế', 'giới']
        self.assertEqual(actual, expected)

    def test_sylabelize_2(self):
        texts = open("tokenize_sets.txt").readlines()
        n = int(len(texts) / 3)
        for i in range(n + 1):
            text = texts[i * 3].strip()
            expected = texts[i * 3 + 1].strip()
            actual_text = " ".join(ViTokenizer.sylabelize(text))
            self.assertEqual(actual_text, expected)

