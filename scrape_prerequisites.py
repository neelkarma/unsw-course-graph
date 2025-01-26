import requests
from bs4 import BeautifulSoup
import json
import re
from time import sleep

COURSE_ID_REGEX = re.compile(r"[A-Z]{4}\d{4}")


def get_prerequisites(course_id: str):
    res = requests.get(
        f"https://www.handbook.unsw.edu.au/undergraduate/courses/2025/{course_id}"
    )

    if not res.ok:
        raise ValueError(
            f"Non-OK status code received: {res.status_code} (probably got ratelimited)"
        )

    soup = BeautifulSoup(res.text, "html.parser")

    el = soup.find(id="__NEXT_DATA__")
    if el is None:
        raise ValueError("__NEXT_DATA__ script tag not found")

    data = json.loads(el.text)
    enrolment_rules = data["props"]["pageProps"]["pageContent"]["enrolment_rules"]
    prerequisites = set()

    for rule in enrolment_rules:
        desc = rule["description"]
        course_ids = COURSE_ID_REGEX.findall(desc)
        prerequisites.update(course_ids)

    return list(prerequisites)


def scrape_prerequisites_bulk(course_codes):
    out = {}
    for i, code in enumerate(course_codes):
        print(f"Fetching prerequisites for {code} ({i + 1}/{len(course_codes)})")
        while True:
            try:
                prereqs = get_prerequisites(code)
                out[code] = prereqs
                break
            except Exception as e:
                print(f"Error fetching prerequisites for {code}: {e}")
                print("Waiting 1 minute before retrying...")
                sleep(60)
                print("Retrying...")

    return out


def main():
    courses = {}
    with open("courses.json") as f:
        courses = json.load(f)

    prereq_data = scrape_prerequisites_bulk(courses.keys())
    with open("prereqs.json", "w") as f:
        json.dump(prereq_data, f, indent=2)


if __name__ == "__main__":
    main()
