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
}
</style>
