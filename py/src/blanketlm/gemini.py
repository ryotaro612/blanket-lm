from google import genai
from google.genai import types
import typing


def load_client(api_key: str) -> genai.client.Client:
    """Creates a client."""
    return genai.Client(api_key=api_key)


class Request(typing.TypedDict):
    """Represents a request to gemini.

    model: e.g., gemini-2.0-flash
    """

    instruction: str
    model: str
    contents: str


def generate_content(client: genai.client.Client, request: Request):
    """ """
    return client.models.generate_content(
        model=request["model"],
        contents=request["contents"],
        config=types.GenerateContentConfig(system_instruction=request["instruction"]),
    )
