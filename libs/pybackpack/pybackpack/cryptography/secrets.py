import string
import secrets


class SecretGenerator:
    """Generate a random secret with given conditions."""

    # Categorize the punctuations into meaningful groups
    quotations = ["'", '"', "`"]
    brackets = ["<", ">", "(", ")", "[", "]", "{", "}"]
    slashes = ["/", "\\"]
    colons = [":", ";"]
    marks = ["!", "?", ".", ","]
    special_chars = [
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "+",
        "=",
        "~",
        "|",
    ]
    safe_chars = ["-", "_"]

    def __init__(
        self,
        length=20,
        number_occurrences=2,
        uppercase_occurrences=2,
        lowercase_occurrences=2,
        punctuation_occurrences=4,
        space_occurrences=0,
        exclude_groups=None,
        alphanumeric=False,
        use_only_safe_chars=False,
    ):
        self.length = length
        self.number_occurrences = number_occurrences
        self.uppercase_occurrences = uppercase_occurrences
        self.lowercase_occurrences = lowercase_occurrences
        self.punctuation_occurrences = punctuation_occurrences
        self.space_occurrences = space_occurrences
        self.exclude_groups = exclude_groups
        self.alphanumeric = alphanumeric
        self.use_safe_chars = use_only_safe_chars

        self.max_retry = 10000

    def generate(self):
        characters = self._get_characters()

        retry_counter = 1
        while True:
            secret = "".join(
                secrets.choice(characters) for x in range(self.length)
            )
            if self._check_secret(secret):
                break

            retry_counter += 1
            if retry_counter == self.max_retry:
                raise ValueError(
                    "Cannot generate secret under given conditions.\
Change the parameters and try again."
                )

        return secret

    def _get_characters(self):
        # If alphanumeric is set, only use alphanumeric characters.
        if self.alphanumeric:
            self.punctuation_occurrences = 0
            self.space_occurrences = 0
            return list(string.ascii_letters + string.digits)

        # If safe_chars_only is set, only use alphanumeric and safe_chars.
        if self.use_safe_chars:
            self.space_occurrences = 0
            return list(
                string.ascii_letters + string.digits + "".join(self.safe_chars)
            )

        # Default occurrences of character groups.
        characters = []
        if self.number_occurrences > 0:
            characters += list(string.digits)
        if self.uppercase_occurrences > 0:
            characters += list(string.ascii_uppercase)
        if self.lowercase_occurrences > 0:
            characters += list(string.ascii_lowercase)
        if self.punctuation_occurrences > 0:
            characters += list(string.punctuation)
        if self.space_occurrences > 0:
            characters.append(" ")

        # Remove characters from excluded groups.
        if self.exclude_groups:
            for group_name in self.exclude_groups:
                group_attr = getattr(self, group_name, None)
                if group_attr:
                    characters = [x for x in characters if x not in group_attr]

        return characters

    def _check_secret(self, secret):
        punctuations = sum(1 for x in secret if x in string.punctuation)
        numbers = sum(1 for x in secret if x in string.digits)
        lowercase = sum(1 for x in secret if x in string.ascii_lowercase)
        uppercase = sum(1 for x in secret if x in string.ascii_uppercase)
        spaces = secret.count(" ")

        return all(
            [
                punctuations >= self.punctuation_occurrences,
                numbers >= self.number_occurrences,
                lowercase >= self.lowercase_occurrences,
                uppercase >= self.uppercase_occurrences,
                spaces >= self.space_occurrences,
            ]
        )
