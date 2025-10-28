<template>
  <div class="project-map-container">
    <div class="shadow-container">
      <h3>Map Filters</h3>
      <div class="checkbox-row">
        <select style="margin-left: -2px" id="county-select" v-model="selectedCounty" @change="zoomToCounty">
        <option value="">All Counties</option>
        <option v-for="county in counties" :key="county" :value="county">{{ county }}</option>
      </select>
      <select id="project-elements" v-model="selectedProjectElement" @change="filterByProjectElement">
        <option value="">All Project Types</option>
        <option v-for="element in projectElements" :key="element" :value="element">{{ element }}</option>
      </select>
      <select id="project-funding" v-model="selectedProjectFunding" @change="filterByProjectFunding">
        <option value="">All Funding Sources</option>
        <option v-for="funding in projectFunding" :key="funding" :value="funding">{{ projectFundingDisplay[funding] }}</option>
      </select>
        <label style="margin-left:1em;">
          <input type="checkbox" v-model="showTransitLayer" @change="toggleTransitLayer" />
          Show Public Transit Layer
        </label>
        <label style="margin-left:1em;">
          <input type="checkbox" v-model="showPopChoropleth" @change="togglePopChoropleth" />
          Show Population Layer
        </label>
      </div>
    </div>
    
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
const showPopChoropleth = ref(false);
let popChoroplethLayer = null;
let popChoroplethGeojson = null;
let popByTract = null;

function getColorForPop(value, min, max) {
  // White to dark green
  if (value == null) return '#fff';
  const percent = (value - min) / (max - min);
  // interpolate from white (255,255,255) to dark green (0,80,0)
  const r = Math.round(255 * (1 - percent));
  const g = Math.round(255 * (1 - percent) + 80 * percent);
  const b = Math.round(255 * (1 - percent));
  return `rgb(${r},${g},${r})`;
}

async function addPopChoroplethLayer() {
  if (popChoroplethLayer) {
    map.value.removeLayer(popChoroplethLayer);
    popChoroplethLayer = null;
  }
  // Fetch and parse data if not already loaded
  if (!popChoroplethGeojson) {
    const geojsonResp = await fetch('/data/vt-census-tract.geojson');
    popChoroplethGeojson = await geojsonResp.json();
  }
  if (!popByTract) {
    await new Promise((resolve) => {
      Papa.parse('/data/vt-pop-by-census-tract.csv', {
        download: true,
        header: true,
        complete: (results) => {
          popByTract = {};
          results.data.forEach(row => {
            // Remove geoId/ prefix
            const id = (row['Entity DCID'] || '').replace('geoId/', '');
            popByTract[id] = parseInt(row['Variable observation value'], 10);
          });
          resolve();
        }
      });
    });
  }
  // Find min/max for color scale
  const popVals = Object.values(popByTract).filter(v => !isNaN(v));
  const minPop = Math.min(...popVals);
  const maxPop = Math.max(...popVals);

  // Attach population to geojson features
  popChoroplethGeojson.features.forEach(f => {
    const tractId = (f.properties.GEOID || f.properties.geoid || f.properties.geoid10 || '').toString();
    f.properties._pop = popByTract[tractId] || null;
  });

  popChoroplethLayer = L.geoJSON(popChoroplethGeojson, {
    style: feature => ({
      fillColor: getColorForPop(feature.properties._pop, minPop, maxPop),
      weight: 1,
      opacity: 1,
      color: '#888',
      fillOpacity: 0.7
    }),
    onEachFeature: function (feature, layer) {
      const pop = feature.properties._pop != null ? feature.properties._pop.toLocaleString() : null;
      layer.bindPopup(`<b>Census Tract:</b> ${feature.properties["County_Name"]}<br><b>Population:</b> ${pop != null ? pop : 'N/A'}`);
    }
  });
  popChoroplethLayer.addTo(map.value);
  // Always send choropleth to the very back
  popChoroplethLayer.bringToBack();
  // If transit layer is present, bring it above choropleth
  if (transitLayer) {
    transitLayer.bringToFront();
    transitLayer.bringToBack(); // ensures it's above choropleth but below markers
  }
  // Markers will always be on top since they're added as L.marker
}

function removePopChoroplethLayer() {
  if (map.value && popChoroplethLayer) {
    map.value.removeLayer(popChoroplethLayer);
    popChoroplethLayer = null;
  }
}

function togglePopChoropleth() {
  if (showPopChoropleth.value) {
    addPopChoroplethLayer();
  } else {
    removePopChoroplethLayer();
  }
}
import { onUnmounted } from 'vue';
const showTransitLayer = ref(false);
let transitLayer = null;
let transitGeojson = null;
import { ref, onMounted } from 'vue';
import { defineEmits } from 'vue';
import L from 'leaflet';
import Papa from 'papaparse';
// import USlideover from Nuxt

const emit = defineEmits(['marker-click']);


const csvUrl = '/data/tdm-geo-clean-photos-20250923.csv'; // Adjust path if needed

const map = ref(null);
const markers = ref([]);
const counties = ref([]);
const selectedCounty = ref('');
const selectedProjectElement = ref('');
const selectedProjectFunding = ref('');
const projectElements = ref(['Sidewalk', 'Repaving', 'Transit', 'Beacon', 'Bike Lane', 'Multi-use', 'Rec trail', 'Bike share']);
const projectFunding = ref(['DTF', 'MTI', 'BP', 'TAP']);

const projectFundingDisplay = {
  DTF: "Downtown Transportation Fund",
  MTI: "Mobility & Transportation Innovations",
  BP: "Bike & Pedestrian Grant Program",
  TAP: "Transportation Alternatives Program"
};


function toggleTransitLayer() {
  console.log('toggleTransitLayer called, checked:', showTransitLayer.value);
  if (showTransitLayer.value) {
    addTransitLayer();
  } else {
    removeTransitLayer();
  }
}

function addTransitLayer() {
  if (!map.value || !transitGeojson) return;
  if (transitLayer) {
    map.value.removeLayer(transitLayer);
  }
  // Deep clone geojson to avoid mutating original
  const geojsonCopy = JSON.parse(JSON.stringify(transitGeojson));

  // Helper to check and fix coordinate order
  function fixCoords(coords) {
    // If array of arrays (MultiLineString or Polygon)
    if (Array.isArray(coords[0])) {
      return coords.map(fixCoords);
    }
    // If single coordinate pair
    if (coords.length === 2 && Math.abs(coords[0]) > Math.abs(coords[1])) {
      // Likely [lon, lat], do nothing
      return coords;
    } else if (coords.length === 2) {
      // If [lat, lon], swap
      return [coords[1], coords[0]];
    }
    return coords;
  }

  geojsonCopy.features.forEach(feature => {
    if (feature.geometry && feature.geometry.coordinates) {
      feature.geometry.coordinates = fixCoords(feature.geometry.coordinates);
    }
  });

  transitLayer = L.geoJSON(geojsonCopy, {
    style: feature => ({
      color: `#${feature.properties.route_color || '2c7bb6'}`,
      weight: 2,
      opacity: 0.7
    }),
    onEachFeature: function (feature, layer) {
      if (feature.properties && feature.properties.route_long_name) {
        layer.bindPopup(`<b>Transit Route:</b> ${feature.properties.route_long_name}`);
      }
    }
  });

  transitLayer.addTo(map.value);
  // Bring transit above choropleth but below markers
  if (popChoroplethLayer) {
    transitLayer.bringToFront();
    popChoroplethLayer.bringToBack();
  } else {
    transitLayer.bringToBack();
  }
}

function removeTransitLayer() {
  if (map.value && transitLayer) {
    map.value.removeLayer(transitLayer);
    transitLayer = null;
  }
}

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
    'primary bike': '#C4B7CB',       
    'mixed use': '#E2C044',          
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

function applyFilters() {
  if (!map.value) return;
  
  // Remove all existing markers from map
  markers.value.forEach(marker => {
    map.value.removeLayer(marker);
  });
  
  // Start with all projects
  let filteredProjects = projects.value;
  
  // Apply project element filter if selected
  if (selectedProjectElement.value) {
    filteredProjects = filteredProjects.filter(project => {
      const projectElements = project['PROJECT ELEMENTS (CODE)'];
      if (!projectElements) return false;
      const elements = projectElements.split(';').map(e => e.trim());
      const lowercasedElements = elements.map(e => e.toLowerCase());
      return lowercasedElements.includes(selectedProjectElement.value.toLowerCase());
    });
  }
  
  // Apply project funding filter if selected
  if (selectedProjectFunding.value) {
    filteredProjects = filteredProjects.filter(project => {
      const projectFundingCode = project['PROJECT FUNDING (CODE)'];
      if (!projectFundingCode) return false;
      const fundingSources = projectFundingCode.split(';').map(f => f.trim());
      const lowercasedFunding = fundingSources.map(f => f.toLowerCase());
      return lowercasedFunding.includes(selectedProjectFunding.value.toLowerCase());
    });
  }
  
  console.log('Filtered projects count:', filteredProjects.length);
  
  // Add filtered markers back to map
  markers.value = filteredProjects.map(project => {
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
      <b>Type:</b> ${projectNumberToName[project['CODE FOR COLOR']]}<br>
      <em>${project['DESCRIPTION (sidewalk, bike lane, length, etc)']}</em><br>
      <b>Completed in:</b> ${project['YEAR COMPLETED'] || 'N/A'}<br>
    `);

    marker.on('mouseover', function () {
      marker.openPopup();
    });
    marker.on('mouseout', function () {
      marker.closePopup();
    });

    marker.on('click', () => {
      emit('marker-click', project);
    });

    return marker;
  });
  
  // Force map to invalidate size and redraw
  map.value.invalidateSize();
}

function filterByProjectElement() {
  applyFilters();
}

function filterByProjectFunding() {
  applyFilters();
}

onMounted(() => {
  Papa.parse(csvUrl, {
    download: true,
    header: true,
    delimiter: ",", // force comma as delimiter
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

      // Add transit geojson layer (initially hidden)
      fetch('/data/vcgi-public-transit.geojson')
        .then(res => res.json())
        .then(geojson => {
          console.log('Fetched transit geojson:', geojson);
          transitGeojson = geojson;
          if (showTransitLayer.value) {
            addTransitLayer();
          }
        });

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
          <b>Type:</b> ${projectNumberToName[project['CODE FOR COLOR']]}<br>
          <em>${project['DESCRIPTION (sidewalk, bike lane, length, etc)']}</em><br>
          <b>Completed in:</b> ${project['YEAR COMPLETED'] || 'N/A'}<br>
        `);

        // Show popup on hover
        marker.on('mouseover', function () {
          marker.openPopup();
        });
        marker.on('mouseout', function () {
          marker.closePopup();
        });

        // Still emit project data on click
        marker.on('click', () => {
          emit('marker-click', project);
        });

        return marker;
      });
    }
  });
// End of onMounted



onUnmounted(() => {
  removeTransitLayer();
  removePopChoroplethLayer();
});
});
</script>

<style scoped>
select {
  margin-bottom: 1em;
  margin-left: 0.5em;
    padding: 0.5em; 
    font-size: 1em
}

#county-zoom {
  margin-left: 1em;
 
}

.legend-overlay {
  position: absolute;
  top: 25%;
  right: 40px;
  z-index: 1000;
  background: rgba(249, 249, 249, 0.95);
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1em;
  max-width: 240px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Ensure parent div is positioned relative */
div {
  position: relative;
} 

.project-map-container {
  margin: 20px;
}
.legend-overlay h3 {
   margin-top: 0;
   font-size: 1.1em;
   margin-bottom: 0.5em;
 }
@media (max-width: 600px) {
  .project-map-container {
  margin: 10px;
}
  .legend-overlay {
    top: auto;
    bottom: 20px;
    right: 20px;
    left: 20px;
    max-width: none;
    font-size: 0.8em;
  }
}

.checkbox-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 1em;
}
@media (max-width: 600px) {
  select {
    margin-left: 0em
  }
  .checkbox-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5em;
  }
  .checkbox-row label {
    margin-left: 0 !important;
  }
}

/* make checkboxes larger */
input[type="checkbox"] {
  width: 16px;
  height: 16px;
  vertical-align: middle;
  margin-right: 0.25em;
}

.shadow-container {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1em;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #fdfdfd;
}
 
</style>