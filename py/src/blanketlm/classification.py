import argparse
import sys
from google import genai
import logging
from google.genai import types
import csv
import typing


def parse(args: list[str]):
    ...

    parser = argparse.ArgumentParser()
    parser.add_argument("meta")
    parser.add_argument("genapi_key")
    parser.add_argument("output")

    return parser.parse_args(args)


def load_client(api_key: str) -> genai.client.Client:
    """ """
    return genai.Client(api_key=api_key)


class Post(typing.TypedDict):
    """ """

    en: str | None
    ja: str | None


def read_posts(file: str) -> dict[str, Post]:
    with open(file) as f:
        records = list(csv.DictReader(f))
        res = dict()
        for record in records:
            res[record["name"]] = {
                "en": record["en"] if record["en"] else None,
                "ja": record["ja"] if record["ja"] else None,
            }
        return res


class Inference(typing.TypedDict):
    model: str
    contents: str
    instruction: str
    result: str


def generate_content(client: genai.client.Client, contents: str) -> Inference:
    """ """
    instruction = (
        "Does the title of the above text come from a research paper, "
        "and is the body a summary of that paper? If so, print 'yes'; otherwise, print 'no'. "
        "The output must be either 'yes' or 'no'."
    )
    model = "gemini-2.0-flash"
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=instruction),
    )
    return {
        "model": model,
        "contents": contents,
        "instruction": instruction,
        "result": response.model_dump_json(),
    }


def classify(args: list[str]):
    """ """
    options = parse(args)
    # empty cell is read as an empty string

    """
    Does the title of the above text come from a research paper, 
    and is the body a summary of that paper? If so, print 'yes'; otherwise, print 'no'. 
    The output must be either 'yes' or 'no'."

    https://googleapis.github.io/python-genai/genai.html#genai.models.Models.generate_content
    """
    client = load_client(options.genapi_key)

    posts = read_posts(options.meta)

    output_file = options.output

    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "model", "contents", "instruction", "result"])
        for name, post in posts.items():
            content_file = post["ja"] or post["en"]

            if not content_file:
                continue

            with open(content_file) as cf:
                contents = cf.read()

            logging.debug(f"Classifying {name}...")
            inference = generate_content(client, contents)
            writer.writerow(
                [
                    name,
                    inference["model"],
                    inference["contents"],
                    inference["instruction"],
                    inference["result"],
                ]
            )


def _classify():
    """ """
    logging.basicConfig(level=logging.DEBUG)
    classify(sys.argv[1:])
