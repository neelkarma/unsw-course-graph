import json


def main():
    courses = {}
    with open("courses.json") as f:
        courses = json.load(f)

    course_prereqs = {}
    with open("course-prereqs.json") as f:
        course_prereqs = json.load(f)

    specialisations = {}
    with open("specialisations.json") as f:
        specialisations = json.load(f)

    specialisation_courses = {}
    with open("specialisation-courses.json") as f:
        specialisation_courses = json.load(f)

    combined_courses = {
        code: {"title": title, "prereqs": course_prereqs.get(code, [])}
        for code, title in courses.items()
    }
    combined_specialisations = {
        code: {"title": title, "courses": specialisation_courses.get(code, [])}
        for code, title in specialisations.items()
    }

    with open("./webpage/src/lib/assets/data.json", "w") as f:
        json.dump(
            {"courses": combined_courses, "specialisations": combined_specialisations},
            f,
            indent=2,
        )


if __name__ == "__main__":
    main()
