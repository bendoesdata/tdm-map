<template>
  <div class="bar-chart-container">
    <h3>Projects Completed by Year</h3>
    <div class="bar-chart">
      <div
        v-for="year in sortedYears"
        :key="year"
        class="bar-item"
      >
        <div class="bar-wrapper">
          <div
            class="bar"
            :style="{ height: barHeight(counts[year]) + 'px' }"
          >
            <span class="bar-count">{{ counts[year] }}</span>
          </div>
        </div>
        <div class="bar-label">{{ year }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Papa from 'papaparse';

const csvUrl = '/data/tdm-geo-clean-20250911.csv';
const counts = ref({});
const sortedYears = ref([]);

function barHeight(count) {
  const maxHeight = 140; // px, adjust as needed
  return Math.min(maxHeight, Math.max(16, count * 5));
}

onMounted(() => {
  Papa.parse(csvUrl, {
    download: true,
    header: true,
    complete: (results) => {
      const yearCounts = {};
      // remove entry if YEAR COMPLETED is "Since 2019"
      results.data = results.data.filter(row => row['YEAR COMPLETED'] !== 'Since 2019');
      results.data.forEach(row => {
        const year = row['YEAR COMPLETED'];
        if (year && year.trim() !== '') {
          yearCounts[year] = (yearCounts[year] || 0) + 1;
        }
      });
      counts.value = yearCounts;
      sortedYears.value = Object.keys(yearCounts).sort();
    }
  });
});
</script>

<style scoped>

.bar-chart-container {
  max-width: 600px;
  width: 100%;
  margin: 2em auto;
  padding: 1em;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  overflow-x: auto;
}
.bar-chart {
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  gap: 18px;
  min-height: 180px;
  padding-bottom: 0.5em;
  overflow-x: auto;
}
.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  min-width: 38px;
}
.bar-label {
  margin-bottom: 0.2em;
  font-size: 0.95em;
  color: #333;
  word-break: break-word;
  text-align: center;
}
.bar-wrapper {
  display: flex;
  align-items: flex-end;
  height: 100px;
}
.bar {
  width: 32px;
  background: #587B7F;
  border-radius: 6px 6px 0 0;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  color: #fff;
  font-weight: bold;
  font-size: 1em;
  transition: height 0.3s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.bar-count {
  margin-bottom: 6px;
}

@media (max-width: 800px) {
  .bar-chart-container {
    max-width: 100vw;
    padding: 0.5em;
  }
  .bar-chart {
    gap: 8px;
    padding-bottom: 1em;
  }
  .bar-item {
    min-width: 32px;
  }
  .bar {
    width: 24px;
    font-size: 0.85em;
  }
  .bar-wrapper {
    height: 70px;
  }
}

@media (max-width: 600px) {
  .bar-chart-container {
    max-width: 100vw;
    width: 100vw;
    margin-left: -8px;
    margin-right: -8px;
    padding: 0.5em;
    overflow-x: visible;
  }
  .bar-chart {
    gap: 8px;
    padding-bottom: 1em;
  }
  .bar-item {
    min-width: 32px;
  }
  .bar {
    width: 20px;
  }
  .bar-wrapper {
    height: 70px;
  }
}
</style>
