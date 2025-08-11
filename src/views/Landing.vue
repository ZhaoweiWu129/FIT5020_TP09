<template>
  <div>
    <Navbar />
    <HeroSection />
    <RouteMap/>
    <Footer/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import HeroSection from '@/components/HeroSection.vue'
import Footer from '@/components/Footer.vue'
import RouteMap from '@/components/RouteMap.vue'

export default {
  name: 'LandingPage',
  components: {
    Navbar,
    HeroSection,
    RouteMap,
    Footer
  }
}
</script>


