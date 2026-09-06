import unittest
from p5_Farafonov_Daniel import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):

    def test_caesar_cipher(self):
        self.assertEqual(caesar_cipher("abc", 1), "bcd")

    def test_caesar_decipher(self):
        self.assertEqual(caesar_decipher("bcd", 1), "abc")

    def test_letter_frequency(self):
        self.assertEqual(letter_frequency("Aab!"), {"a": 2, "b": 1})


if __name__ == "__main__":
    unittest.main()
