<template>
  <nav class="navbar">
    <!-- Left: Brand -->
    <router-link to="/" class="brand">
      <img src="@/assets/Logo1_cropped.png" alt="AgilePark logo" class="brand__logo" />
    </router-link>

    <!-- Hamburger button (visible on mobile) -->
    <button class="hamburger" @click="toggleMenu" aria-label="Toggle menu">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- Right: Navigation links -->
    <!-- <div class="nav-links">
      <router-link to="/" class="nav-item">Home</router-link>
      <router-link to="/route" class="nav-item">Park & Ride options</router-link>
      <router-link to="/data-insight" class="nav-item">Data Insights</router-link>
    </div> -->
    <!-- Navigation links -->
    <div class="nav-links" :class="{ open: menuOpen }">
      <router-link to="/" class="nav-item" @click="menuOpen = false">Home</router-link>
      <router-link to="/route" class="nav-item" @click="menuOpen = false">Park & Ride options</router-link>
      <router-link to="/data-insight" class="nav-item" @click="menuOpen = false">Data Insights</router-link>
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
  /* align-items: center; */
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

.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  margin-left: auto;
  z-index: 100;
  padding: 6px;
  width: 44px;
  height: 44px;
}

.hamburger span {
  display: block;
  height: 4px;
  width: 100%;
  background: #2563eb;
  border-radius: 2px;
  transition: 0.3s;
}

@media (max-width: 960px) {

  .brand__logo {
    height: 40px; /* smaller logo */
  }

  .nav-item {
    font-size: 1rem; /* smaller text on mobile */
    padding: 8px 16px; /* space inside each link */
  }

  .hamburger {
    display: flex;
  }

  .nav-links {
    display: none;
    flex-direction: column;
    gap: 12px;
    width: calc(100% - 20px);;
    background: #1e1e2f; /* darker, modern look */
    padding: 12px 0;
    border-radius: 8px;
    position: absolute;
    justify-content: center;
    top: 60px;
    left: 0;
    margin: 20px 12px; /* space from edges of screen */
    transition: all 0.3s ease;
    transform: translateY(-20px);
    z-index: 99;
  }

  .nav-links.open {
    display: flex;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2); /* subtle shadow */
  }

  .navbar {
    position: relative;
    flex-direction: row;
    align-items: center;
    padding: 10px 8px;
  }

  .hamburger span {
    height: 3px;
  }
}

</style>
<script setup lang="ts">

import { ref } from 'vue';
const menuOpen = ref(false);
function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

</script>