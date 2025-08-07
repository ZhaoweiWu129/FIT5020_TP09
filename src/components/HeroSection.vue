<template>
  <section class="hero">
    <div class="hero-container">
      <div class="hero-text">
        <p class="small-title">Neque porro quisquam est qui dolorem ipsum quia</p>
        <h1 class="main-title">MELBOURNE PARKING</h1>
        <p class="description">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
          Ut enim ad minim veniam, quis nostrud exercitation.
        </p>
        <div class="buttons">
          <button class="btn-primary">Find out more</button>
          <button class="btn-secondary">See all cars ownership</button>
        </div>
      </div>

      <div class="hero-image">
        <div class="image-placeholder"></div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HeroSection'
}
</script>

<style scoped>
.hero {
  background-color: #dce3ed;
  padding: 80px 20px;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
}

.hero-text {
  flex: 1;
  min-width: 300px;
  padding-right: 40px;
}

.small-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.main-title {
  font-size: 36px;
  font-weight: bold;
  color: #1e1e1e;
  margin-bottom: 20px;
}

.description {
  font-size: 16px;
  color: #444;
  margin-bottom: 30px;
}

.buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.btn-primary {
  background-color: white;
  color: black;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  border-radius: 6px;
  font-weight: bold;
}

.btn-secondary {
  background-color: transparent;
  color: black;
  padding: 10px 20px;
  border: 2px solid black;
  cursor: pointer;
  border-radius: 6px;
  font-weight: bold;
}

.hero-image {
  flex: 1;
  min-width: 300px;
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.image-placeholder {
  width: 100%;
  max-width: 400px;
  height: 280px;
  background-color: #a1aaba;
  border-radius: 30px;
}
</style>
