<template>
  <nav class="navbar">
    <div class="navbar-content">
      <h1 class="logo">AgilePark</h1>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
.navbar {
  background-color: rgba(243, 243, 243, 0.49);
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.logo {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}
</style>
