import sys
import logging
import os.path
import requests
import csv


def _retrieve(args: list[str]):
    logging.basicConfig(level=logging.DEBUG)
    links_csv = args[0]
    dest_dir = args[1]
    result_csv = args[2]

    with open(links_csv) as f, open(result_csv, "w") as success_file:
        links = [r for r in csv.DictReader(f)]

        result_writer = csv.writer(success_file)
        result_writer.writerow(["name", "sucecss"])

        for link in links:
            ok = False
            try:
                logging.debug(f"Retrieving {link['name']}: {link['url']}")
                res = requests.get(link["url"])
                if res.ok:
                    for k, v in res.headers.items():
                        if k.lower() == "content-type" and "pdf" in v.lower():
                            with open(
                                os.path.join(dest_dir, f"{link["name"]}.pdf"), "wb"
                            ) as f:
                                f.write(res.content)
                                ok = True
                                break
            except Exception as e:
                logging.error(f"Failed to retrieve {link['name']}, {link['url']}: {e}")

            finally:
                result_writer.writerow([link["name"], "true" if ok else "false"])


def retrieve():
    _retrieve(sys.argv[1:])
