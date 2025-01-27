import sys
import requests
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_hydration_data.py <url>")
        exit(1)

    url = sys.argv[1]
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    el = soup.find(id="__NEXT_DATA__")

    if el is None:
        print("__NEXT_DATA__ script tag not found")
        exit(1)

    print(el.text)


if __name__ == "__main__":
    main()
