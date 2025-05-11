import argparse
from os import path
import os
import dataclasses


@dataclasses.dataclass
class Website:
    """ """

    def __init__(self, basedir: str):
        self.basedir = basedir

    @property
    def files(self):
        dir = path.join(self.basedir, "content", "posts")
        ls = os.listdir(dir)
        print(ls)


def parse(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("website")
    parser.add_argument("output")
    return parser.parse_args(args)


def _markdown(args: list[str]):
    namespace = parse(args)
    website = Website(namespace.website)

    website.files

    print("doge")
