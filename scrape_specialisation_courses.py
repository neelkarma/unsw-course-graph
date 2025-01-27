import requests
from bs4 import BeautifulSoup
import json
from time import sleep


def scrape_specialisation_courses(specialisation_code: str):
    res = requests.get(
        f"https://www.handbook.unsw.edu.au/undergraduate/specialisations/2025/{specialisation_code}"
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
    curriculum_structure = data["props"]["pageProps"]["pageContent"][
        "curriculumStructure"
    ]["container"]

    course_ids = set()
    for stage in curriculum_structure:
        # don't ask - this is how the data is structured
        course_groups = stage["container"]
        for group in course_groups:
            courses = group["relationship"]
            for course in courses:
                if "academic_item_code" in course:
                    course_id = course["academic_item_code"]
                    course_ids.add(course_id)

        courses = stage["relationship"]
        for course in courses:
            if "academic_item_code" in course:
                course_id = course["academic_item_code"]
                course_ids.add(course_id)

    return list(course_ids)


def scrape_specialisation_courses_bulk(specialisation_codes):
    out = {}
    for i, code in enumerate(specialisation_codes):
        print(
            f"Scraping prerequisites for {code} ({i + 1}/{len(specialisation_codes)})"
        )
        while True:
            try:
                courses = scrape_specialisation_courses(code)
                print(code, courses)
                out[code] = courses
                break
            except Exception as e:
                print(f"Error scraping prerequisites for {code}: {e}")
                print("Waiting 1 minute before retrying...")
                sleep(60)
                print("Retrying...")

    return out


def main():
    specialisations = {}
    with open("specialisations.json") as f:
        specialisations = json.load(f)

    course_data = scrape_specialisation_courses_bulk(specialisations.keys())
    with open("specialisation-courses.json", "w") as f:
        json.dump(course_data, f, indent=2)


if __name__ == "__main__":
    main()
