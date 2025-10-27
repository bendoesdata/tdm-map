<template>
  <div>
    <div class="flex items-start gap-4 intro-section" style="width: 100%;">
      <div class="intro-text">
        <div style="margin-top: 20px">
          <p>This map presents initiatives built and implemented around Vermont since 2019 that are making it easier for residents to get around their communities without a car. This review focused on changes to infrastructure of all sizes and scopes, from installation of rectangular rapid flashing beacons that improve pedestrian crossing safety, to construction of cross-community multi-use paths. There are also projects that help Vermonters use alternatives to single-occupancy vehicles, like e-bike libraries, expanded transit centers, and micro-transit systems.</p>
          <br>
          <p>Some of these projects started at the state level, others were initiated by a handful of community members. This survey likely does not capture every change to Vermont infrastructure that supports bikes and pedestrians since 2019. However, it does provide a sample of the types of projects that have been realized across Vermont communities. Explore the map to see details, funding sources, and agencies and groups involved with each specific project.</p>
          <br>
        </div>
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
            v-if="selectedProject && selectedProject.photo"
            :src="'/images/' + selectedProject.photo + '.jpg'"
            alt="Project Image"
            class="project-image"
          />
          <span v-if="selectedProject['photo credit']" class="caption">{{ 'Photo courtesty of ' + (selectedProject['photo credit'] ? selectedProject['photo credit'] : '') }}</span>
        </div>
        <br></br>
        <div>

        </div>
        <div v-if="selectedProject">
          <div>
            <h3>{{ selectedProject['LOCATION OF PROJECT'] ? selectedProject['LOCATION OF PROJECT'] : 'Not available' }}</h3>
            <p>{{ selectedProject['DESCRIPTION (sidewalk, bike lane, length, etc)'] ? selectedProject['DESCRIPTION (sidewalk, bike lane, length, etc)'] : 'Not available' }}</p>
          </div>
          <br></br>
          <hr></hr>
          <br></br>
          <div v-for="key in displayKeys" :key="key" style="margin-bottom: 0.5em;">
            <strong>{{ keyNames[key] || key }}: </strong>
            <div style="display: inline-block" v-if="key === 'PROJECT ELEMENTS (CODE)'">
              <template v-if="selectedProject[key]">
                  <span v-for="element in selectedProject[key].split(';')" :key="element" class="pill-box" :style="{ backgroundColor: elementColors[element.trim().toLowerCase()] || '#000' }">
                    {{ element.trim() }}
                  </span>
              </template>
              <template v-else>
                Not available
              </template>
            </div>
            <span v-else-if="key !== 'RELEVANT LINKS - FACT SHEETS'">
              <template v-if="key === 'PROJECT FUNDING (CODE)'">
                {{ fundingDisplay[selectedProject[key]] || selectedProject[key] || 'Not available' }}
              </template>
              <template v-else>
                {{ selectedProject[key] ? selectedProject[key] : 'Not available' }}
              </template>
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
    <div class="credits">
      This research was funded through the Vermont Agency of Transportation’s Mobility and Transportation Innovations Grant.
    </div>
  </div>
</template>

<script setup>
import ProjectMap from '../components/ProjectMap.vue';
import YearBarChart from '../components/YearBarChart.vue';
import { ref } from 'vue';

const selectedProject = ref(null);
const slideoverOpen = ref(false);

const elementColors = {
  "bike lane": "#C4B6CB",
  "sidewalk": "#577B7F",
  "crosswalk": "#577B7F",
  "multi-use": "#e5b402",
  "bike share": "#C4B6CB",
  "beacon": "#577B7F",
  "rec trail": "#e5b402",
  "transit": "#393E41",
  "repaving": "#393E41"
};

const fundingDisplay = {
  DTF: "Downtown Transportation Fund",
  MTI: "Mobility & Transportation Innovations",
  BP: "Bike & Pedestrian Grant Program",
  TAP: "Transportation Alternatives Program"
}

const displayKeys = [
  "CITY",
  "PROJECT ELEMENTS (CODE)",
  "PROJECT FUNDING (CODE)",
  "YEAR COMPLETED",
  "TOTAL COST (where available)",
  "PROJECT AGENCY OR INVOLVED GROUPS (where available)",
  "RELEVANT LINKS - FACT SHEETS"
];

const keyNames = {
  "CITY": "City",
  "PROJECT ELEMENTS (CODE)": "Project Elements",
  "PROJECT FUNDING (CODE)": "Project Funding",
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
