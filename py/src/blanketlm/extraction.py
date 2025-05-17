import sys
import csv


instruction = r"""
You will be given a summary of a research paper that contains a link to the paper.  
Extract the URL from the text and download the PDF. The link may point directly to a PDF or to a web page that contains a link to the PDF.
"""


def extract(args: list[str]):
    summary_csv = args[0]
    posts_csv = args[1]

    with open(summary_csv) as summary_file:
        names = {r["name"] for r in csv.DictReader(summary_file)}

    with open(posts_csv) as posts_file:
        posts = csv.DictReader(posts_file)
        summary_posts: list[str] = [
            post["ja"] for post in posts if post["name"] in names
        ]

    return summary_posts


def _extract():
    extract(sys.argv[1:])
