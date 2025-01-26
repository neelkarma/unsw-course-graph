import requests
import json


def fetch_course_data():
    start = 0
    courses = {}
    while True:
        print(f"Fetching course data (currently at {start})")
        res = requests.post(
            "https://api-ap-southeast-2.prod.courseloop.com/publisher/search-academic-items",
            json={
                "siteId": "unsw-prod-pres",
                "query": "",
                "contenttype": "subject",
                "searchFilters": [
                    {
                        "filterField": "studyLevelValue",
                        "filterValue": ["ugrd"],
                        "isExactMatch": False,
                    },
                    {
                        "filterField": "implementationYear",
                        "filterValue": ["2025"],
                        "isExactMatch": False,
                    },
                    {
                        "filterField": "active",
                        "filterValue": ["1"],
                        "isExactMatch": False,
                    },
                ],
                "from": start,
                "size": 100,
            },
        )

        data = res.json()["data"]["results"]

        if len(data) == 0:
            break

        for course in data:
            courses[course["code"]] = course["title"]

        start += 100

    return courses


def main():
    courses = fetch_course_data()
    with open("courses.json", "w") as f:
        json.dump(courses, f, indent=2)


if __name__ == "__main__":
    main()
