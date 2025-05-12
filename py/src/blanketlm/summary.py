import csv
import sys
import json


def filter_summary(args: list[str]):
    classification_file = args[0]
    white_list = {
        "universal_language_model_fine_tuning_for_text_classification",
        "statistics_and_causal_inference",
        "sagas",
        "hyperdex",
        "automatic_differentiation_in_pytorch",
        "your_coffee_shop_doesnt_use_two_phase_commit",
        "the_annotated_transformer",
        "universal_language_model_fine_tuning_for_text_classification",
    }
    with open(classification_file) as f:
        records = list(csv.DictReader(f))

        summaries = []
        for record in records:
            if (
                "yes"
                in json.loads(record["result"])["candidates"][0]["content"]["parts"][0][
                    "text"
                ]
                or record["name"] in white_list
            ):
                summaries.append(
                    {
                        "name": record["name"],
                        "contents": record["contents"],
                    }
                )
    summary_file = args[1]
    with open(summary_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        writer.writerows([[r["name"]] for r in summaries])


def _filter_summary():
    filter_summary(sys.argv[1:])
