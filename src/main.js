import Vue from 'vue'
import App from './App.vue'
import router from './nav'
import 'leaflet/dist/leaflet.css';

Vue.config.productionTip = false


router.afterEach((to) => {
  document.title = to.meta.title || 'Default Title';
});

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')