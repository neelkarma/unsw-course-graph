# UNSW Course Graph

## Usage

Make sure the following are installed:

- Python 3
- `uv`
- NodeJS
- `pnpm`

Run these commands in order:

```sh
$ uv sync                                            # install python deps
$ uv venv                                            # create a virtual environment
$ source .venv/bin/activate                          # activate the virtual environment
$ python fetch_courseloop_data.py courses            # fetch course data
$ python fetch_courseloop_data.py specialisations    # fetch specialisation data
$ python scrape_course_prerequisites.py              # scrape course prerequisites - this will take a while
$ python scrape_specialisation_courses.py            # scrape specialisation courses - this will also take a while
$ python make_graph.py                               # generate the graph data json
$ cd website                                         # navigate to the website directory
$ pnpm i                                             # install node deps
$ pnpm build                                         # build the website
$ pnpm preview                                       # serve the website (open the url shown in the terminal)
```

The website build is configured to output a single HTML file, so you can also
serve `webpage/build/index.html` with any static file server.

## How it works

`fetch_courseloop_data.py` fetches the names and codes of all specialisations
and courses from the UNSW handbook using the CourseLoop Search API used in
[this page](https://www.handbook.unsw.edu.au/search) (check the network tab in
browser devtools). It saves the data to `courses.json` and
`specialisations.json`.

`scrape_course_prerequisites.py` fetches the page for each course in
`courses.json`, and extracts the prerequisites from the JSON data embedded in
the pages. It saves the data to `course-prereqs.json`.

`scrape_specialisation_courses.py` fetches the page for each specialisation in
`specialisations.json`, and extracts the courses related to the specialisation.
It saves the data to `specialisation-courses.json`.

`make_graph.py` combines the data from `courses.json`, `course-prereqs.json`,
`specialisations.json`, and `specialisation-courses.json` into a JSON file saved
in `website/src/lib/assets/data.json`. This JSON file is used by the website, a
Svelte app, to visualize the graph.

## Acknowledgements

- [Graphology](https://graphology.github.io/) - Graph data structure library
- [Sigma.js](https://sigmajs.org) - Graph visualization library
- [Svelte](https://svelte.dev) - Web framework
