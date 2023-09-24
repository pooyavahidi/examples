import string
from pybackpack.cryptography.secrets import SecretGenerator


def test_generate_strong_pass():
    length = 20
    number_occurrences = 2
    uppercase_occurrences = 2
    lowercase_occurrences = 2
    punctuation_occurrences = 2
    space_occurrences = 0
    pass_gen = SecretGenerator(
        length=length,
        number_occurrences=number_occurrences,
        uppercase_occurrences=uppercase_occurrences,
        lowercase_occurrences=lowercase_occurrences,
        punctuation_occurrences=punctuation_occurrences,
        space_occurrences=space_occurrences,
    )

    # Check the length of the password to be equal to the given length
    password = pass_gen.generate()
    assert len(password) == length

    punctuations = 0
    numbers = 0
    uppercase = 0
    lowercase = 0
    spaces = 0

    for x in password:
        punctuations += len([y for y in string.punctuation if x == y])
        numbers += len([y for y in string.digits if x == y])
        lowercase += len([y for y in string.ascii_lowercase if x == y])
        uppercase += len([y for y in string.ascii_uppercase if x == y])
        spaces += 1 if x == " " else 0

    assert punctuations >= punctuation_occurrences
    assert numbers >= number_occurrences
    assert lowercase >= lowercase_occurrences
    assert uppercase >= uppercase_occurrences
    assert spaces >= space_occurrences
