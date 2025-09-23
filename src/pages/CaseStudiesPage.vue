<template>
  <div class="case-studies-page">
    <h1>Case Studies</h1>
    <SimpleAccordion :items="caseStudies" />
    <router-link to="/">Back to Home</router-link>
  </div>
</template>

<script setup>
import SimpleAccordion from '../components/SimpleAccordion.vue';

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

<style scoped>
.case-studies-page {
  max-width: 700px;
  margin: 2em auto;
  padding: 2em;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
</style>
