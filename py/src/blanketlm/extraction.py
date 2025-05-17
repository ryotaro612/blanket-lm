import sys
import json
import blanketlm.gemini as gemini
import csv


instruction = (
    "You'll receive a Markdown summary of a research paper, which may include several links. "
    "Extract and provide only the URL of the paper being summarized. "
    "Your response should be a single line containing this URL."
)


def extract(args: list[str]):
    summary_csv = args[0]
    posts_csv = args[1]
    key = args[2]

    output_csv = args[3]

    with open(summary_csv) as summary_file:
        names = {r["name"] for r in csv.DictReader(summary_file)}

    res = []
    with open(posts_csv) as posts_file:
        posts = csv.DictReader(posts_file)
        summary_posts = [post for post in posts if post["name"] in names]

    client = gemini.load_client(key)
    with open(output_csv, "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["name", "url"])
        for summary_post in summary_posts:
            with open(summary_post["ja"]) as f:
                contents = f.read()
                res = gemini.generate_content(
                    client,
                    {
                        "instruction": instruction,
                        "model": "gemini-2.0-flash",
                        "contents": contents,
                    },
                )
                url = json.loads(res.model_dump_json())["candidates"][0]["content"][
                    "parts"
                ][0]["text"].strip()
            writer.writerow([summary_post["name"], url])


def _extract():
    extract(sys.argv[1:])
