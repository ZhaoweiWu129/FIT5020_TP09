<template>
  <section class="popular">
    <h2>Popular Parking Spaces</h2>
    <div class="parking-list">
      <div class="card">Little Collins Street - $25/day</div>
      <div class="card">Flinders Lane - $30/day</div>
      <div class="card">Russell Street - $22/day</div>
      <div class="card">King Street - $20/day</div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'PopularSection'
}
</script>

<style scoped>
.popular {
  padding: 60px 20px;
  background-color: #fafafa;
  text-align: center;
}

.parking-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  padding: 20px;
  width: 200px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
</style>
