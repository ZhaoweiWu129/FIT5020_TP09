<template>
  <nav class="navbar">
    <!-- Left: Brand -->
    <router-link to="/" class="brand">
      <img src="@/assets/Logo1_cropped.png" alt="AgilePark logo" class="brand__logo" />
    </router-link>

    <!-- Right: Navigation links -->
    <div class="nav-links">
      <router-link to="/" class="nav-item">Home</router-link>
      <router-link to="/route" class="nav-item">Park and ride</router-link>
      <router-link to="/data-insight" class="nav-item">Data Insight</router-link>
    </div>
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

/* Constrain the logo size */
.brand__logo {
  height: 40px;
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
.navbar {
  display: flex;
  justify-content: space-between; /* pushes logo left, links right */
  align-items: center;
  padding: 12px 20px;
}

.brand__logo {
  height: 60px; /* adjust size */
  width: auto;
}

.nav-links {
  display: flex;
  gap: 70px; /* space between nav items */
  padding-right: 100px;
}

.nav-item {
  text-decoration: none;
  color: inherit;
  font-weight: 500;
  font-size: 1.5rem;
}

.nav-item:hover {
  text-decoration: underline;
}
</style>
<script setup lang="ts">
</script>