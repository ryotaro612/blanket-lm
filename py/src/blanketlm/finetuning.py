import sys
import os.path
import csv
import logging
from google import genai
import pymupdf4llm
from google.genai import types


def _read_dataset(posts_file: str, papers_dir: str):
    dataset = []
    with open(posts_file) as f:
        records = list(csv.DictReader(f))

        for record in records:

            logging.debug(f"Processing {record}")
            paper_path = f"{os.path.join(papers_dir, record['name'])}.pdf"

            if not os.path.exists(paper_path):
                continue

            text = pymupdf4llm.to_markdown(paper_path)
            with open(record["ja"]) as f:
                summary = f.read()

            instruction = "\n\n以上の文書をMarkdown形式で要約してください。"
            dataset.append([f"{text}{instruction}", summary])

    return dataset


def _finetune(args: list[str]):
    logging.basicConfig(level=logging.DEBUG)

    posts_file = args[0]
    papers_dir = args[1]

    dataset = _read_dataset(posts_file, papers_dir)

    training_dataset = types.TuningDataset(
        examples=[
            types.TuningExample(
                text_input=i,
                output=o,
            )
            for i, o in dataset
        ],
    )

    client = genai.Client()  # Get the key from the GOOGLE_API_KEY env variable

    # tuning_job = client.tunings.tune(
    #     base_model="models/gemini-2.0-flash",
    #     training_dataset=training_dataset,
    #     config=types.CreateTuningJobConfig(
    #         epoch_count=5,
    #         batch_size=4,
    #         learning_rate=0.001,
    #         tuned_model_display_name="test tuned model",
    #     ),
    # )
    # return tuning_job


def _main():
    _finetune(sys.argv[1:])
