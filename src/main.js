import { createApp } from 'vue'
import App from './App.vue'
import 'leaflet/dist/leaflet.css';
import ui from '@nuxt/ui/vue-plugin'
import router from './router'

import './assets/main.css'

createApp(App).use(ui).use(router).mount('#app')