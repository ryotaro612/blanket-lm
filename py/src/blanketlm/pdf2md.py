import sys
import os.path
import pymupdf4llm
import logging


def _extract(args: list[str]):
    paper_dir = args[0]
    md_dir = args[1]

    for paper in os.listdir(paper_dir):
        if not paper.endswith(".pdf") or paper in {
            "a_comparative_study_of_programming_languages_in_rosetta_code.pdf"
        }:
            continue

        logging.debug(f"Processing {paper}")
        md_path = os.path.join(md_dir, f"{paper[:-4]}.md")
        if os.path.exists(md_path):
            continue

        paper_path = os.path.join(paper_dir, paper)
        text = pymupdf4llm.to_markdown(paper_path)
        if not text:
            continue

        with open(md_path, "w") as f:
            f.write(text)


def _main():
    logging.basicConfig(level=logging.DEBUG)
    _extract(sys.argv[1:])
