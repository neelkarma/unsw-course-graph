import requests
import json
import sys


def fetch_all(contenttype: str, display_name: str):
    start = 0
    out = {}
    while True:
        print(f"Fetching all {display_name} (currently at {start})")
        res = requests.post(
            "https://api-ap-southeast-2.prod.courseloop.com/publisher/search-academic-items",
            json={
                "siteId": "unsw-prod-pres",
                "query": "",
                "contenttype": contenttype,
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

        for item in data:
            out[item["code"]] = item["title"]

        start += 100

    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: fetch_courseloop_data.py (courses | specialisations)")
        exit(1)

    data_type = sys.argv[1]
    contenttype = ""
    match data_type:
        case "courses":
            contenttype = "subject"
        case "specialisations":
            contenttype = "aos"
        case _:
            print(
                f"Unknown data type: {data_type} (must be one of 'courses' or 'specialisations')"
            )
            exit(1)

    data = fetch_all(contenttype, data_type)
    with open(f"{data_type}.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
