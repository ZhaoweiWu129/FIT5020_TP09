<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- Logo + description -->
      <div class="footer-left">
        <div class="footer-brand">
          <img src="@/assets/Logo1.png" alt="ParkAgile Logo" class="footer-logo" />
          <span class="footer-name">ParkAgile</span>
        </div>
        <p class="footer-description">
          Our vision is to provide convenience and help increase your parking efficiency.
        </p>

      </div>

      <!-- Link sections -->
      <div class="footer-links">

      </div>
    </div>

    <!-- Bottom line -->
    <div class="footer-bottom">
      <p>©2025 TP09. All rights reserved</p>
      <div class="policy-links">
        <a href="#">Privacy & Policy</a>
        <a href="#">Terms & Condition</a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background-color: rgb(14, 14, 19);
  padding: 40px 20px 20px;
  margin: 0%;
  max-width: 100%;
  font-family: sans-serif;
  color: #868686;
}

.footer-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  max-width: 88vw;
  margin: auto;
  gap: 40px;
}

.footer-left {
  flex: 1;
  min-width: 220px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.description {
  font-size: 14px;
  color: #555;
  margin-bottom: 15px;
}

.social-icons a {
  margin-right: 10px;
  color: #333;
  font-size: 16px;
  text-decoration: none;
}

.footer-links {
  display: flex;
  flex: 2;
  justify-content: space-between;
  min-width: 400px;
  gap: 30px;
}

.footer-links h4 {
  font-size: 16px;
  margin-bottom: 10px;
}

.footer-links ul {
  list-style: none;
  padding: 0;
}

.footer-links li {
  margin-bottom: 8px;
}

.footer-links a {
  text-decoration: none;
  color: #333;
  font-size: 14px;
}

.footer-bottom {
  border-top: 1px solid #ccc;
  margin-top: 30px;
  padding-top: 15px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  max-width: 88vw;
  margin-left: auto;
  margin-right: auto;
  font-size: 13px;
  color: #666;
}

.policy-links a {
  margin-left: 20px;
  text-decoration: none;
  color: #666;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px; /* space before description */
}

.footer-logo {
  height: 28px; /* adjust to match navbar */
  width: auto;
}

.footer-name {
  font-weight: 700;
  font-size: 1.125rem;
  letter-spacing: 0.2px;
}

</style>
