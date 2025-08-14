<template>
  <div id="app" class="app-shell">
    <Navbar />
    <main class="app-content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: 'App',
  components: {
    // eslint-disable-next-line vue/no-unused-components
    Navbar,Footer
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
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-content {
  flex: 1;
  display: block;
}
</style>
