# UNSW Course Graph

## Usage

1. Make sure Python and `pip` are installed.
2. Install the required packages:

```sh
pip install -r requirements.txt
```

3. Run `fetch_course_data.py` and wait for it to complete.
4. Run `scrape_prerequisites.py` and wait for it to complete. This will take a
   while (> 40 min), since UNSW ratelimits requests to their handbook.
5. Run `make_graph.py`.
6. Open the generated `graph.html` file in a browser.

## How it works

`fetch_course_data.py` fetches the names and codes of all courses from the UNSW
handbook using the CourseLoop Search API used in
[this page](https://www.handbook.unsw.edu.au/search) (check the network tab in
browser devtools). It saves the data to `courses.json`.

`scrape_prerequisites.py` fetches the page for each course in `courses.json`,
and extracts the prerequisites from the JSON data embedded in the page. It saves
the data to `prerequisites.json`.

`generate_graph.py` embeds the data from `courses.json` and `prereqs.json` into
`template.html`, which uses the data to visualize the graph data using
[Sigma.js](https://www.sigmajs.org). The new HTML file with the embedded data is
saved to `graph.html`.
