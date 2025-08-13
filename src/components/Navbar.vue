<!-- Navbar.vue -->
<template>
  <nav class="navbar">
    <router-link to="/" class="brand">
      <img src="@/assets/Logo1_cropped.png" alt="AgilePark logo" class="brand__logo" />
    </router-link>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  padding: 0px 20px;
}

/* Make logo + text stay on one line and center-align vertically */
.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
  line-height: 1;
}

/* Constrain the logo size so it doesn't dominate */
.brand__logo {
  height: 8vh;
  margin: 1vh 0px;
  width: auto;
  display: block;
}

/* Make the name look like a proper brand */
.brand__text {
  font-weight: 900;
  font-size: 1.125rem;     /* ~18px */
  letter-spacing: .2px;
}
</style>
<script setup lang="ts">
</script>