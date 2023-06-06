import sys
import json
import boto3

region_name = "us-east-1"


def detect_entities(text):
    comprehend = boto3.client(
        service_name="comprehend", region_name=region_name
    )

    response_entities = comprehend.detect_entities(
        Text=text, LanguageCode="en"
    )

    return response_entities["Entities"]


def redact(text, entities):
    entities_dict = {}
    entity_counters = {}

    entities_sorted = sorted(
        entities, key=lambda x: x["BeginOffset"], reverse=True
    )
    for entity in entities_sorted:
        if entity["Text"] not in entity_counters:
            entity_counters[entity["Text"]] = len(entity_counters) + 1

        # Create Variables with the format such as {{PERSON1}}.
        variable = f"{{{{{entity['Type']}{entity_counters[entity['Text']]}}}}}"
        entities_dict[variable] = entity["Text"]
        text = (
            text[: entity["BeginOffset"]]
            + variable
            + text[entity["EndOffset"] :]
        )
    return text, entities_dict


def reveal(text, entities_dict):
    for variable, entity in entities_dict.items():
        text = text.replace(variable, entity)
    return text


def reveal_file(file_name):
    # Read entities
    with open(file_name + ".entities", "r", encoding="utf-8") as f:
        entity_dict = json.load(f)

    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()
        text = "".join(lines)

    revealed = reveal(text, entities_dict=entity_dict)
    return revealed


def redact_file(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()
        text = "".join(lines)

    entities = detect_entities(text)
    redacted, entity_dict = redact(text, entities=entities)

    # Write entities to a file
    with open(file_name + ".entities", "w", encoding="utf-8") as f:
        json.dump(entity_dict, f)

    return redacted, entity_dict


def test():
    test_text = """Hello, my name is John Doe. My date of birth is 1/1/75.
and my email is johndoe@example.com. John Doe is here."""

    entities = detect_entities(test_text)
    new_text, entity_dict = redact(test_text, entities)
    print("Original text:")
    print(test_text)
    print("-" * 79)
    print("Redacted text:")
    print(new_text)
    print("-" * 79)
    print("Entities:")
    print(entity_dict)
    print("-" * 79)

    original_text = reveal(new_text, entity_dict)
    print("Revealed text:")
    print(original_text)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["redact", "reveal", "test"],
        default="test",
        help="Command to execute",
    )
    parser.add_argument("-f", "--file-name", help="Input file name")
    parser.add_argument("-t", "--text", help="Input text")

    # Handle the case where no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.command == "redact":
        if args.file_name:
            redacted, entity_dict = redact_file(args.file_name)
            print(redacted)
        elif args.text:
            entities = detect_entities(args.text)
            new_text, entity_dict = redact(args.text, entities)
            print(new_text)
        else:
            print("Please provide either file name or text for redact command")

    elif args.command == "reveal":
        if args.file_name:
            revealed_text = reveal_file(args.file_name)
            print(revealed_text)
        elif args.text:
            print("Error: The --text option is not supported.")
        else:
            print("Please provide either file name or text for reveal command")

    elif args.command == "test":
        test()
