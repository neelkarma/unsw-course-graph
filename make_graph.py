import json


def main():
    courses = {}
    with open("courses.json") as f:
        courses = json.load(f)

    prereqs = {}
    with open("prereqs.json") as f:
        prereqs = json.load(f)

    combined = []
    for code in courses:
        prereq = prereqs.get(code, [])
        combined.append({"code": code, "title": courses[code], "prereqs": prereq})

    template = ""
    with open("template.html") as f:
        template = f.read()

    graph = template.replace("{{ data }}", json.dumps(combined))

    with open("graph.html", "w") as f:
        f.write(graph)


if __name__ == "__main__":
    main()
