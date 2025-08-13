<template>
  <div>
    <label for="county-select">Zoom to County:</label>
    <select id="county-select" v-model="selectedCounty" @change="zoomToCounty">
      <option value="">All Counties</option>
      <option v-for="county in counties" :key="county" :value="county">{{ county }}</option>
    </select>
    <div id="map" style="height: 600px; margin-top: 1em; position: relative;"></div>
    <div class="legend-overlay">
      <h3>Project Type Legend</h3>
      <ul>
        <li v-for="(color, type) in projectColors" :key="type" style="list-style:none; margin-bottom:0.5em; display:flex; align-items:center;">
          <span :style="{background: color, width: '16px', height: '16px', borderRadius: '50%', display: 'inline-block', marginRight: '0.5em', border: '2px solid #fff'}"></span>
          <span>{{ type }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import L from 'leaflet';
import Papa from 'papaparse';

const csvUrl = '/data/tdm_walk_score.csv'; // Adjust path if needed

const map = ref(null);
const markers = ref([]);
const counties = ref([]);
const selectedCounty = ref('');

// dict to translate project number to name
const projectNumberToName = {
    1: 'primary pedestrian',
    2: 'primary bike',
    3: 'mixed use',
    4: 'primary other transit'
};

// dict to translate project types to colors
const projectColors = {
    'primary pedestrian': '#587B7F', 
    'primary bike': '#E2C044',       
    'mixed use': '#C4B7CB',          
    'primary other transit': '#393E41'
};

const projects = ref([]);

function getCountyBounds(county) {
  const points = projects.value.filter(p => p.COUNTY.trim() === county)
    .map(p => [parseFloat(p.LAT), parseFloat(p.LON)]);
  if (points.length === 0) return null;
  return L.latLngBounds(points);
}

function zoomToCounty() {
  if (!selectedCounty.value) {
    map.value.flyTo([44.0, -72.7], 8, { animate: true, duration: 1.5 }); // Vermont center
    return;
  }
  const bounds = getCountyBounds(selectedCounty.value);
  if (bounds) map.value.flyToBounds(bounds, { maxZoom: 12, animate: true, duration: 1.5 });
}

onMounted(() => {
  Papa.parse(csvUrl, {
    download: true,
    header: true,
    complete: (results) => {
      projects.value = results.data.filter(row => row.LAT && row.LON);
      counties.value = [...new Set(projects.value.map(p => p.COUNTY.trim()))].sort();

      // convert project types to colors
      projects.value.forEach(project => {
        const projectType = project['CODE FOR COLOR'];
        project['COLOR'] = projectColors[projectNumberToName[projectType]] || '#000000'; // default to black if not found
      });

      map.value = L.map('map', {
        center: [44.0, -72.7], // Vermont
        zoom: 8,
        zoomControl: true,
        attributionControl: false,
      });

      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors © CARTO',
      }).addTo(map.value);

      // Add markers with color styling
      markers.value = projects.value.map(project => {
        const markerIcon = L.divIcon({
          className: 'custom-marker',
          html: `<div style="background:${project.COLOR};width:16px;height:16px;border-radius:50%;border:2px solid #fff;"></div>`,
          iconSize: [20, 20],
          iconAnchor: [10, 10],
        });

        const marker = L.marker([parseFloat(project.LAT), parseFloat(project.LON)], {
          title: project['LOCATION OF PROJECT FOR TEXT'] || project['ADDRESS OF PROJECT TO MAP'],
          icon: markerIcon,
        }).addTo(map.value);

        marker.bindPopup(`
          <strong>${project['LOCATION OF PROJECT FOR TEXT'] || project['ADDRESS OF PROJECT TO MAP']}</strong><br>
          <em>${project['DESCRIPTION (sidewalk, bike lane, length, etc)']}</em><br>
          <b>Type:</b> ${projectNumberToName[project['CODE FOR COLOR']]}<br>
          <b>Completed in:</b> ${project['YEAR COMPLETED'] || 'N/A'}<br>
          <b>Total cost:</b> $${project['TOTAL COST (where available)'] || 'N/A'}<br>
        `);
        return marker;
      });
    }
  });
});
</script>

<style scoped>
#county-select {
  margin-bottom: 1em;
  margin-left: 0.5em;
    padding: 0.5em; 
    font-size: 1em
}

 .legend-overlay {
   position: absolute;
   top: 30%;
   right: 100px;
   z-index: 1000;
   background: rgba(249, 249, 249, 0.95);
   border: 1px solid #ddd;
   border-radius: 8px;
   padding: 1em;
   max-width: 240px;
   box-shadow: 0 2px 8px rgba(0,0,0,0.08);
 }
 .legend-overlay h3 {
   margin-top: 0;
   font-size: 1.1em;
   margin-bottom: 0.5em;
 }
</style>