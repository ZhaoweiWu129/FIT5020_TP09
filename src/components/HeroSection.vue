<template>

  <section class="hero">

    <!-- Background video -->
    <video
      ref="bgVideo"
      class="hero-bg-video"
      autoplay
      muted
      playsinline
      @ended="playNextVideo"
    ></video>

    <div class="hero__band">
      <div class="hero__grid">
        <div class="hero__left">
          <h1 class="hero__title">Park & <span class="thin"> Ride</span></h1>
          <p class="hero__lead">
            We provide Park & Ride options based on your route to the CBD and your preferences. <br/>
            Just drive to a train station along your route, park your car, and hop on the train to the CBD.
          </p>
          <button @click="goToRoute" class="find-route-btn">
            Find Park & Ride Options Along Your Route
          </button>
          <button @click="goToData" class="find-route-btn">
            View Data Insights
          </button>
        </div>
        <!-- <div class="hero__right">
          <img src="@/assets/Hero.jpg" alt="front" class = "front" />
        </div> -->

      </div>
    </div>
  </section>
</template>

<style scoped>
:root{
  --ink:#121418;
  --muted:#616975;
}

video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}

.hero__band {
  position: relative;
  z-index: 2; /* on top of video */
  color: white;
}

.hero {
  min-height: 88vh; /* nearly full viewport height */
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-size: cover;
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 18px 50px rgba(0,0,0,.12);
  position: relative; /* Needed for absolute positioning of button */
  text-align: center;
  top: 1px;
  margin: 0vh 0.8vw;
}

.hero::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.753) 0%, rgba(24, 28, 38, 0.0) 70%);
}

.hero__grid, .hero__wrap, .hero__inner {
  /* max-width: 1200px; */
  margin: 0 auto;
  padding: clamp(56px, 7vw, 110px) 28px;
  display: grid;
  grid-template-columns: 7fr 5fr;  /* stronger emphasis on text */
  align-items: center;
  gap: clamp(28px, 4vw, 64px);
}

/* Left column: stronger headline & tighter measure */
.hero__left{
  max-width: 560px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.hero__title{
  font-weight: 900;
  letter-spacing: -0.02em;
  line-height: 1.04;
  font-size: clamp(52px, 7.5vw, 92px);
  margin: 0 0 14px;
  color: var(--ink);
  text-align: left; /* Align title to the left */
}

.hero__lead{
  color: var(--muted);
  font-size: clamp(16px, 1.9vw, 20px);
  line-height: 1.7;
  text-align: left;
  margin: 0 0 26px;
}

.hero__actions{ display:flex; gap:12px; flex-wrap:wrap; }
.btn{ padding: 14px 18px; border-radius: 10px; font-weight: 700; }

/* Right column */
.hero__right{
  position: relative;
  justify-self: end;
  width: min(520px, 38vw);
  height: min(640px, 48vw);
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 18px 50px rgba(0,0,0,.12);
  background: #f6f7f9;

  perspective: 1200px;
  transition: transform 1.2s ease;
  transform-style: preserve-3d;
}

/* spin on hover (optional) */
.hero__right:hover{
  transform: rotateY(360deg);
}

/* FRONT image */
.hero__right img{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;

  backface-visibility: hidden;
  transition: opacity .6s ease;  /* allow crossfade */
  z-index: 2;                    /* above ::after by default */
}
/* Fade overlay */
.hero__right::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(to left, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 30%);
  z-index: 1;
  pointer-events: none; /* let clicks go through */
}
/* BACK image*/
.hero__right::after{
  content: "";
  position: absolute;
  inset: 0;
  background-image: url('../assets/hero3.jpg');
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity .6s ease .15s;
  z-index: 1;                    /* below <img> at start */
}

/* CROSSFADE on hover */
.hero__right:hover img{ opacity: 0; }     /* fade front out */
.hero__right:hover::after{ opacity: 1; }  /* fade back in */

.down-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(43, 43, 43, 0.452);
  border: none;
  position: absolute;
  left: 50%;
  bottom: 18px;
  transform: translateX(-50%);
  width: 98%;
  z-index: 10;
  cursor: pointer;
  transition: filter 0.2s;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  border-radius: 12px;
}

.down-arrow:hover {
  background: rgba(39, 39, 39, 0.521);
}

.topbar, header.navbar, .site-header{
  background:#f3f4f6;
}

/* Tighten page edges (browsers add default margin) */
:global(html, body){ margin:0; }

/* Responsive stack */
@media (max-width: 980px){
  .hero__grid, .hero__wrap, .hero__inner{
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 44px 20px;
  }
  .hero__right{
    width: 100%;
    height: 300px;
    justify-self: stretch;
  }
}

.find-route-btn {
  background-color: rgba(127, 127, 165, 0.486);
  color: rgb(255, 255, 255);
  padding: 12px 20px;
  /* margin: 0 12px; */
  margin-top: 1.5rem;
  font-size: 1.1rem;
  font-weight: 500;
  border: none;
  gap: 2px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  min-width: 0;
  flex-shrink: 1;
}
.find-route-btn:hover {
  background-color: #627baa;
}
</style>

<script setup>
import { ref, onMounted } from 'vue';

const videos = [
  require('@/assets/vid/train1.mp4'),
  require('@/assets/vid/train2.mp4'),
  require('@/assets/vid/train3.mp4')
];
const currentIndex = ref(0);
const bgVideo = ref(null);

function playVideo(index) {
  const videoEl = bgVideo.value;
  if (videoEl) {
    videoEl.src = videos[index];
    videoEl.play().catch(err => {
      console.error("Video play failed:", err);
    });
  }
}

function playNextVideo() {
  currentIndex.value = (currentIndex.value + 1) % videos.length;
  playVideo(currentIndex.value);
}

onMounted(() => {
  playVideo(currentIndex.value);
});


</script>

<script>
export default {
  name: 'HeroSection',
  methods: {
    goToRoute() {
      this.$router.push('/route')
    },
    goToData() {
      this.$router.push('/data-insight')
    }
  }
}
</script>