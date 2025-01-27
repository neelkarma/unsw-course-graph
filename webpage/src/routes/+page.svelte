<script>
  import Sigma from "sigma";
  import { DirectedGraph } from "graphology";
  import { circular } from "graphology-layout";
  import FA2Layout from "graphology-layout-forceatlas2/worker";
  import { inferSettings } from "graphology-layout-forceatlas2";
  import { courses, specialisations } from "$lib/assets/data.json";
  import { hslToHex } from "$lib";
  import { SvelteSet } from "svelte/reactivity";
  import Filter from "./Filter.svelte";

  let graphContainer = $state();
  let selectedSpecialisations = $state(new SvelteSet());
  let sigma;
  let layout;

  $effect(() => {
    let filteredCourses = Object.entries(courses).map(
      ([code, { title, prereqs }]) => ({ code, title, prereqs }),
    );

    if (selectedSpecialisations.size > 0) {
      const includedCourses = new Set();
      for (const specialisation of selectedSpecialisations) {
        for (const code of specialisations[specialisation].courses) {
          includedCourses.add(code);
        }
      }

      filteredCourses = filteredCourses.filter(({ code }) =>
        includedCourses.has(code),
      );
    }

    const graph = new DirectedGraph();
    const colorMap = new Map();

    const addNode = (code, label) => {
      const category = code.substring(0, 4);

      if (!colorMap.has(category)) {
        const hue = Math.floor(Math.random() * 360);
        colorMap.set(category, hslToHex(hue, 100, 50));
      }

      graph.addNode(code, {
        label,
        color: colorMap.get(category),
        size: 4,
      });
    };

    for (const { code, title } of filteredCourses) {
      addNode(code, `${code} - ${title}`);
    }

    for (const { code, prereqs } of filteredCourses) {
      for (const prereq of prereqs) {
        if (!graph.hasNode(prereq)) {
          console.warn(`Node ${prereq} not found - adding`);
          addNode(prereq, prereq);
        }

        graph.addEdge(prereq, code, {
          color: "gray",
          size: 2,
        });
      }
    }

    circular.assign(graph);
    layout = new FA2Layout(graph, {
      settings: inferSettings(graph),
    });
    layout.start();

    sigma = new Sigma(graph, graphContainer, {
      labelColor: { color: "gray" },
      defaultEdgeType: "arrow",
    });

    sigma.on("enterNode", ({ node }) => {
      graph.setNodeAttribute(node, "size", 7);
      graph.setNodeAttribute(node, "forceLabel", true);
      graph.forEachNeighbor(node, (other) => {
        graph.setNodeAttribute(other, "size", 7);
        graph.setNodeAttribute(other, "forceLabel", true);
        try {
          graph.setEdgeAttribute(node, other, "color", "cyan");
        } catch {
          graph.setEdgeAttribute(other, node, "color", "red");
        }
      });
      sigma.refresh();
    });

    sigma.on("leaveNode", ({ node }) => {
      graph.setNodeAttribute(node, "size", 4);
      graph.setNodeAttribute(node, "forceLabel", false);
      graph.forEachNeighbor(node, (other) => {
        graph.setNodeAttribute(other, "size", 4);
        graph.setNodeAttribute(other, "forceLabel", false);
        try {
          graph.setEdgeAttribute(node, other, "color", "gray");
        } catch {
          graph.setEdgeAttribute(other, node, "color", "gray");
        }
      });
      sigma.refresh();
    });

    sigma.on("clickNode", ({ node }) => {
      window.open(
        `https://www.handbook.unsw.edu.au/undergraduate/courses/2025/${node}`,
        "_blank",
      );
    });

    return () => {
      sigma.kill();
      layout.kill();
    };
  });
</script>

<Filter bind:selectedSpecialisations />
<div
  id="container"
  style="width: 100vw; height: 100vh;"
  bind:this={graphContainer}
></div>
