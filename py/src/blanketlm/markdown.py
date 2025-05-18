from collections import defaultdict
import sys
import csv
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
    def posts_dir(self):
        """
        Returns the path to the posts directory.

        """
        return path.join(self.basedir, "content", "posts")

    @property
    def filenames(self):
        """
        Returns absolute paths to all files in the content/posts directory.

        """
        return [f for f in os.listdir(self.posts_dir) if f.endswith(".md")]

    @property
    def posts(self):
        """
        Returns a content written in Japanese or English.

        """
        filenames = self.filenames

        posts: dict[str, dict[str, str | None]] = defaultdict(
            lambda: {"en": None, "ja": None}
        )

        for filename in filenames:
            filepath = path.join(self.posts_dir, filename)
            if filename.endswith("en.md"):
                name = filename[:-6]
                lang = "en"
            elif filename.endswith("ja.md"):
                name = filename[:-6]
                lang = "ja"
            else:
                name = filename[:-3]
                lang = "ja"

            posts[name][lang] = filepath

        return posts


def parse(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("website")
    parser.add_argument("output")
    return parser.parse_args(args)


def write_posts(dest_file, posts: dict[str, dict[str, str | None]]):
    with open(dest_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "en", "ja"])
        for name, post in posts.items():
            writer.writerow([name, post["en"], post["ja"]])


def find_markdown(args: list[str]):
    namespace = parse(args)
    website = Website(namespace.website)
    write_posts(namespace.output, website.posts)


def _markdown():
    find_markdown(sys.argv[1:])
