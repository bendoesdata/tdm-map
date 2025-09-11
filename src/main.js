import { createApp } from 'vue'
import App from './App.vue'
import 'leaflet/dist/leaflet.css';
import ui from '@nuxt/ui/vue-plugin'



createApp(App).use(ui).mount('#app')

import './assets/main.css'