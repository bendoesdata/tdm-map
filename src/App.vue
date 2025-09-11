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
</script>

<template id="app">
  <UApp>
    <h1>Transit Demand Management</h1>
    <div class="flex items-start gap-4 intro-section">
      <div style="margin-top: 20px">
      <p>Explore TDM projects across Vermont. Click on map markers for project details.</p>
      <a
        href="https://vtrans.vermont.gov/planning/tdm"
        target="_blank"
        rel="noopener"
      >
        Learn more about TDM
      </a>
      </div>
      <div style="width: 70%;">
      <YearBarChart />
      </div>
    </div>
    
    <ProjectMap @marker-click="handleMarkerClick" />
    <USlideover
      v-model:open="slideoverOpen"
      title="Project Details"
      close-icon="i-lucide-arrow-right"
      class="project-details-slideover"
    >
      <template #body>
        <div>
          <img
            src=""
            alt="Project Image"
            class="img-placeholder"
          />
        </div>
        <div v-if="selectedProject">
          <div v-for="key in displayKeys" :key="key" style="margin-bottom: 0.5em;">
            <strong>{{ keyNames[key] || key }}: </strong>
            <span v-if="key !== 'RELEVANT LINKS - FACT SHEETS'">
              {{ selectedProject[key] ? selectedProject[key] : 'Not available' }}
            </span>
            <span v-else>
              <template v-if="selectedProject[key]">
                <ul class="link-list">
                  <li>
                    <a :href="selectedProject[key]" target="_blank" rel="noopener">
                      {{ selectedProject[key] }}
                    </a>
                  </li>
                  <li v-if="selectedProject['factsheet 2']">
                    <a :href="selectedProject['factsheet 2']" target="_blank" rel="noopener">
                      {{ selectedProject['factsheet 2'] }}
                    </a>
                  </li>
                  <li v-if="selectedProject['factsheet 3']">
                    <a :href="selectedProject['factsheet 3']" target="_blank" rel="noopener">
                      {{ selectedProject['factsheet 3'] }}
                    </a>
                  </li>
                </ul>
              </template>
              <template v-else>
                Not available
              </template>
            </span>
          </div>
        </div>
        <div v-else>
          <em>No project selected.</em>
        </div>
      </template>
    </USlideover>
  </UApp>
</template>
