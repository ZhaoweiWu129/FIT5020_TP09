<template>
  <div>
    <Navbar />
    <HeroSection />
    <MetricsSection />
    <PopularSection />
    <Footer/>
    <RouteMap/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import HeroSection from '@/components/HeroSection.vue'
import MetricsSection from '@/components/MetricsSection.vue'
import PopularSection from '@/components/PopularSection.vue'
import Footer from '@/components/Footer.vue'
import RouteMap from '@/components/RouteMap.vue'

export default {
  name: 'LandingPage',
  components: {
    Navbar,
    HeroSection,
    MetricsSection,
    PopularSection,
    Footer,
    RouteMap
  }
}
</script>
