<template>
  <div class="accordion">
    <div v-for="(item, idx) in items" :key="idx" class="accordion-item">
      <button class="accordion-header" @click="toggle(idx)">
        <span>{{ item.label }}</span>
        <span class="arrow" :class="{ open: openIndex === idx }">&#9660;</span>
      </button>
      <div v-show="openIndex === idx" class="accordion-content">
        <slot :name="'content-' + idx">{{ item.content }}</slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const props = defineProps({
  items: {
    type: Array,
    required: true
  }
});
const openIndex = ref(null);
function toggle(idx) {
  openIndex.value = openIndex.value === idx ? null : idx;
}
</script>

<style scoped>
.accordion {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.accordion-item + .accordion-item {
  border-top: 1px solid #eee;
}
.accordion-header {
  width: 100%;
  text-align: left;
  background: #f7f7f7;
  border: none;
  outline: none;
  padding: 1em;
  font-size: 1.1em;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.accordion-content {
  padding: 1em;
  background: #fff;
  animation: fadeIn 0.2s;
}
.arrow {
  transition: transform 0.2s;
}
.arrow.open {
  transform: rotate(180deg);
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
