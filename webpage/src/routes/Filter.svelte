<script>
  import { specialisations } from "$lib/assets/data.json";

  let { selectedSpecialisations = $bindable() } = $props();

  let input = $state("");
  let results = $derived.by(() => {
    const query = input.toLowerCase();
    if (query.length === 0) return [];

    return Object.entries(specialisations)
      .filter(
        ([code, { title }]) =>
          !selectedSpecialisations.has(code) &&
          (code.toLowerCase().includes(query) ||
            title.toLowerCase().includes(query)),
      )
      .map(([code]) => code);
  });
</script>

{#snippet checkboxItem(code)}
  <li>
    <label>
      <input
        type="checkbox"
        bind:checked={
          () => selectedSpecialisations.has(code),
          (v) => {
            if (v) {
              selectedSpecialisations.add(code);
            } else {
              selectedSpecialisations.delete(code);
            }
          }
        }
      />
      {code} - {specialisations[code].title}
    </label>
  </li>
{/snippet}

<details>
  <summary>Filter</summary>
  <input
    type="text"
    placeholder="Search specialisations..."
    bind:value={input}
  />
  <ul>
    {#each selectedSpecialisations as code}
      {@render checkboxItem(code)}
    {/each}
    {#each results as code}
      {@render checkboxItem(code)}
    {/each}
  </ul>
</details>

<style>
  details {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 99;
    background-color: black;
    border: 1px solid gray;
    padding: 5px;
  }

  summary {
    cursor: pointer;
  }

  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
</style>
