<template>
  <section class="hero">
    <div class="hero__band">
      <div class="hero__grid">
        <div class="hero__left">
          <h1 class="hero__title">Park & <span class="thin"> Ride</span></h1>
          <p class="hero__lead">
            Drive to a nearby station, then ride into the CBD by train, tram, or bus.
          </p>
        </div>
        <div class="hero__right">
          <img src="@/assets/Hero.jpg" alt="front" class = "front" />
        </div>

      </div>
    </div>
  </section>
</template>

<style scoped>
:root{
  --ink:#121418;
  --muted:#616975;
}

.hero {
  background-size: cover;
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 18px 50px rgba(0,0,0,.12);
}

.hero__grid, .hero__wrap, .hero__inner {
  max-width: 1200px;
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
}
.hero__title{
  font-weight: 900;
  letter-spacing: -0.02em;
  line-height: 1.04;
  font-size: clamp(52px, 7.5vw, 92px);
  margin: 0 0 14px;
  color: var(--ink);
}
.hero__lead{
  color: var(--muted);
  font-size: clamp(16px, 1.9vw, 20px);
  line-height: 1.7;
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
</style>

