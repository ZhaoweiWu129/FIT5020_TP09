import Vue from 'vue'
import App from './App.vue'
import router from './nav'
import 'leaflet/dist/leaflet.css';

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')