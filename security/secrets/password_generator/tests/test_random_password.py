import unittest
import string
import timeit

from password_generator.random_password import RandomPassword

class TestPasswordGenerator(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_generate_strong_pass(self):
        length = 20
        number_occurrences = 2
        uppercase_occurrences = 2
        lowercase_occurrences = 2
        punctuation_occurrences = 2
        space_occurrences = 0
        exclude_characters = ""
        pass_gen = RandomPassword(
            length = length,
            number_occurrences = number_occurrences,
            uppercase_occurrences=uppercase_occurrences,
            lowercase_occurrences=lowercase_occurrences,
            punctuation_occurrences=punctuation_occurrences,
            space_occurrences=space_occurrences,
            exclude_characters=exclude_characters
        )
        password = pass_gen.generate()
        print (password)
        self.assertEqual(length, len(password))
        punctuations = 0
        numbers=0
        uppercase = 0
        lowercase = 0
        spaces = 0

        for x in password:
            punctuations += len([y for y in string.punctuation if x==y])
            numbers += len([y for y in string.digits if x==y])
            lowercase += len ([y for y in string.ascii_lowercase if x==y])
            uppercase += len ([y for y in string.ascii_uppercase if x==y])
            spaces += 1 if x == " " else 0

        self.assertGreaterEqual(punctuations, punctuation_occurrences)
        self.assertGreaterEqual(numbers, number_occurrences)
        self.assertGreaterEqual(lowercase, lowercase_occurrences)
        self.assertGreaterEqual(uppercase, uppercase_occurrences)
        self.assertGreaterEqual(spaces, space_occurrences)
