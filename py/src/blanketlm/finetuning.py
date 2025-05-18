import sys
import os.path
import csv
import logging
from google import genai
import pymupdf4llm
from google.genai import types


def _read_dataset(posts_file: str, papers_md_dir: str):
    dataset = []
    with open(posts_file) as f:
        records = list(csv.DictReader(f))

        for record in records:

            logging.debug(f"Processing {record}")
            paper_path = f"{os.path.join(papers_md_dir, record['name'])}.md"

            if not os.path.exists(paper_path):
                continue

            with open(record["ja"]) as f:
                summary = f.read()

            with open(paper_path) as f:
                text = f.read()

            instruction = "以下の文書をMarkdown形式で要約してください。\n\n"
            dataset.append([f"{instruction}{text}", summary, record["name"]])

        dataset.sort(key=lambda e: e[2])
    return [
        d
        for i, d in enumerate(dataset)
        if i not in {47, 69, 114, 33, 47, 91, 46, 89, 146}
    ]


def _finetune(args: list[str]):
    logging.basicConfig(level=logging.DEBUG)

    posts_file = args[0]
    papers_dir = args[1]

    dataset = _read_dataset(posts_file, papers_dir)

    training_dataset = types.TuningDataset(
        examples=[
            types.TuningExample(
                text_input=i[:20000],
                output=o[:4000],
            )
            for i, o, _ in dataset
        ],
    )

    client = genai.Client()  # Get the key from the GOOGLE_API_KEY env variable

    tuning_job = client.tunings.tune(
        base_model="models/gemini-2.0-flash",
        training_dataset=training_dataset,
        config=types.CreateTuningJobConfig(
            epoch_count=5,
            batch_size=4,
            learning_rate=0.001,
            tuned_model_display_name="test tuned model",
        ),
    )
    # return tuning_job


def _main():
    _finetune(sys.argv[1:])
