import string
import secrets
import sys

class RandomPassword:

    # Some examples of supported and unsupported punctuations list
    quotations = ["'",'"']
    unsupported_punctuation_1 = ['<','>',';',"\\"]
    unsupported_punctuation_2 = ['!','@','#','$','%','^','&','*','(',')','.']
    supported_punctuation_1 = ['.', '-','_']

    def __init__(
        self,
        length = 20,
        number_occurrences = 2,
        uppercase_occurrences = 2,
        lowercase_occurrences = 2,
        punctuation_occurrences = 2,
        space_occurrences=0,
        exclude_characters=""):

        self.length = length
        self.number_occurrences = number_occurrences
        self.uppercase_occurrences = uppercase_occurrences
        self.lowercase_occurrences = lowercase_occurrences
        self.punctuation_occurrences = punctuation_occurrences
        self.space_occurrences = space_occurrences
        self.exclude_characters = exclude_characters

        self.max_retry = 1000


    def generate(self):

        characters = []
        if self.number_occurrences > 0:
            characters += string.digits
        if self.uppercase_occurrences > 0:
            characters += string.ascii_uppercase
        if self.lowercase_occurrences > 0:
            characters += string.ascii_lowercase
        if self.punctuation_occurrences > 0:
            characters += string.punctuation
        if self.space_occurrences > 0:
            characters += " "

        characters = [x for x in characters if x not in self.exclude_characters]
        # TODO: After excluding the characters, still we need to check if based on
        # the existing characters, can we generate a password which meets the
        # occurrences conditions (in a reasonable time period). As a workaround, we
        # can rely on max number of retry and then ask consumer to relax the conditions

        # check the password and if the occurrence conditions have not been met
        # retry and generate a new password
        retry_counter = 1
        while True:
            password = "".join(
                secrets.choice(characters) for x in range(self.length)
            )
            if self._check_password(password):
                break

            # raise an error if after maximum tries still password cannot
            # be generated under given conditions
            retry_counter += 1
            if retry_counter == self.max_retry:
                raise Exception(
                    "Cannot generate password under given conditions. "\
                    "Change the parameters and try again")

        return password
    def _check_password(self, password):
        punctuations = 0
        numbers=0
        uppercase = 0
        lowercase = 0
        spaces = 0

        #Todo: Use sum(comprehention) instead of looping through chars
        # https://docs.python.org/3/library/secrets.html
        for x in password:
            punctuations += len([y for y in string.punctuation if x==y])
            numbers += len([y for y in string.digits if x==y])
            lowercase += len ([y for y in string.ascii_lowercase if x==y])
            uppercase += len ([y for y in string.ascii_uppercase if x==y])
            spaces += 1 if x == " " else 0 

        if punctuations < self.punctuation_occurrences:
            return False
        if numbers < self.number_occurrences:
            return False
        if lowercase < self.lowercase_occurrences:
            return False
        if uppercase < self.uppercase_occurrences:
            return False
        if spaces < self.space_occurrences:
            return False

        return True
 
if __name__ == "__main__":
    size = 20
    exclude_characters = ""

    if len(sys.argv) > 1 :
        size = int(sys.argv[1])
    if len(sys.argv) > 2:
        exclude_characters = sys.argv[2]
    pass_gen = RandomPassword(
        length=size,
        #exclude_characters=exclude_characters,
        punctuation_occurrences=3
    )
    p = pass_gen.generate()
    print (p)
