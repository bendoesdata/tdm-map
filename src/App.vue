<script setup>
import ProjectMap from './components/ProjectMap.vue';
import YearBarChart from './components/YearBarChart.vue';
import { ref } from 'vue';

const selectedProject = ref(null);
const slideoverOpen = ref(false);

// array of keys to display in slideover
const displayKeys = [
  "CITY",
  "LOCATION OF PROJECT",
  "YEAR COMPLETED",
  "DESCRIPTION (sidewalk, bike lane, length, etc)",
  "TOTAL COST (where available)",
  "PROJECT AGENCY OR INVOLVED GROUPS (where available)",
  "RELEVANT LINKS - FACT SHEETS"
];

// dictionary with more user-friendly names for keys
const keyNames = {
  "CITY": "City",
  "LOCATION OF PROJECT": "Location of Project",
  "DESCRIPTION (sidewalk, bike lane, length, etc)": "Description",
  "YEAR COMPLETED": "Year Completed",
  "TOTAL COST (where available)": "Total Cost",
  "PROJECT AGENCY OR INVOLVED GROUPS (where available)": "Project Agency or Involved Groups",
  "RELEVANT LINKS - FACT SHEETS": "Links and Fact Sheets"
};

function handleMarkerClick(project) {
  selectedProject.value = project;
  slideoverOpen.value = true;
  console.log('Project clicked:', project, slideoverOpen.value);
}

const caseStudies = [
  {
    label: 'Burlington Greenway Extension',
    content: `The Burlington Greenway Extension project connected the city's popular multi-use path to new neighborhoods, increasing access for both commuters and recreational users. The project included new signage, improved crossings, and community engagement to ensure the path met local needs.`
  },
  {
    label: 'Montpelier Microtransit Pilot',
    content: `Montpelier launched a microtransit pilot in 2023, providing on-demand rides for residents without access to fixed-route transit. The pilot reduced single-occupancy vehicle trips and provided valuable data for future transit planning.`
  },
  {
    label: 'Brattleboro E-Bike Library',
    content: `Brattleboro's E-Bike Library program allowed residents to borrow e-bikes for up to two weeks, encouraging active transportation and reducing car dependency. The program was supported by local businesses and received positive feedback from participants.`
  }
];
</script>

<template id="app">
  <UApp>
    <div class="header-bar">
      <h1>Transit Demand Management</h1>
      <nav>
        <router-link to="/">Home</router-link>
        |
        <router-link to="/case-studies">Case Studies</router-link>
        |
        <router-link to="/about">About</router-link>
      </nav>
    </div>
    <router-view />
  </UApp>
</template>

<style scoped>
.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5em;
}
h1 {
  margin: 0;
  font-size: 2em;
  font-weight: 700;
}
nav {
  text-align: right;
}
nav a {
  margin: 0 0.5em;
  text-decoration: none;
  color: #065d00;
}
@media (max-width: 600px) {
  .header-bar {
    flex-direction: column-reverse;
    align-items: center;
    gap: 0.5em;
  }
  nav {
    text-align: center;
    width: 100%;
  }
  h1 {
    text-align: center;
    font-size: 1.3em;
  }
}
</style>
