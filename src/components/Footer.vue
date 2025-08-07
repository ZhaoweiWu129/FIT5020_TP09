<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- Logo + description -->
      <div class="footer-left">
        <h2 class="logo">Logo</h2>
        <p class="description">
          Our vision is to provide convenience and help increase your parking efficiency.
        </p>
        <div class="social-icons">
          <a href="#"><i class="fab fa-facebook-f"></i></a>
          <a href="#"><i class="fab fa-twitter"></i></a>
          <a href="#"><i class="fab fa-instagram"></i></a>
        </div>
      </div>

      <!-- Link sections -->
      <div class="footer-links">
        <div>
          <h4>About</h4>
          <ul>
            <li><a href="#">How it works</a></li>
            <li><a href="#">Featured</a></li>
            <li><a href="#">Partnership</a></li>
            <li><a href="#">Business Relation</a></li>
          </ul>
        </div>
        <div>
          <h4>Community</h4>
          <ul>
            <li><a href="#">Events</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Podcast</a></li>
            <li><a href="#">Invite a friend</a></li>
          </ul>
        </div>
        <div>
          <h4>Socials</h4>
          <ul>
            <li><a href="#">Discord</a></li>
            <li><a href="#">Instagram</a></li>
            <li><a href="#">Twitter</a></li>
            <li><a href="#">Facebook</a></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Bottom line -->
    <div class="footer-bottom">
      <p>©2025 Company Name. All rights reserved</p>
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
  background-color: #dce3ed;
  padding: 40px 20px 20px;
  font-family: sans-serif;
  color: #333;
}

.footer-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  max-width: 1200px;
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
  max-width: 1200px;
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
</style>
