<template>
  <div id="app">
    <LandingPage />
  </div>
</template>

<script>
import LandingPage from './views/Landing.vue'

export default {
  name: 'App',
  components: {
    LandingPage
  }
}
</script>

<style>
html, body, #app {
  font-family: "Quicksand", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  background: rgb(24, 24, 31);
  color: rgba(255, 255, 255, 0.9);
  margin: 0%;
  padding: 0%;
}
</style>
