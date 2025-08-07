<template>
  <section class="route-map">
    <h2>Find a Route</h2>

    <form @submit.prevent="getRoute">
      <div class="input-group">
        <label>Start (lat,lng)</label>
        <input v-model="startAddress" placeholder="Start address (e.g. 300 Flinders St, Melbourne)" />
      </div>
      <div class="input-group">
        <label>Destination (lat,lng)</label>
        <input v-model="endAddress" placeholder="Destination address (e.g. 50 Lonsdale St, Melbourne)" />
      </div>
      <button type="submit">Get Route</button>
    </form>

    <div v-if="result" class="result">
      <p><strong>Distance:</strong> {{ (result.distance / 1000).toFixed(2) }} km</p>
      <p><strong>Time:</strong> {{ Math.round(result.time / 60000) }} min</p>
    </div>

    <div id="map" ref="map" class="map"></div>
  </section>
</template>

<script>
import L from 'leaflet';

export default {
  name: "RouteMap",
  data() {
    return {
      startAddress: "Flinders Street, Melbourne",
      endAddress: "Russell Street, Melbourne",
      result: null,
      map: null,
      routeLayer: null
    };
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap() {
      this.map = L.map(this.$refs.map).setView([-37.8136, 144.9631], 15);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(this.map);
    },
    async getRoute() {
      const key = "d1ab6ff6-8d5b-4ae6-99a6-d80e046f9826";

      try {
        const [startLat, startLng] = await this.geocode(this.startAddress);

        const [endLat, endLng] = await this.geocode(this.endAddress);

        const url = `https://graphhopper.com/api/1/route?point=${startLat},${startLng}&point=${endLat},${endLng}&vehicle=car&locale=en&calc_points=true&points_encoded=false&key=${key}`;

        const res = await fetch(url);
        const data = await res.json();

        if (data.paths && data.paths.length > 0) {
          const path = data.paths[0];
          this.result = {
            distance: path.distance,
            time: path.time
          };

          const coords = path.points.coordinates.map(coord => [coord[1], coord[0]]);
          if (this.routeLayer) this.routeLayer.remove();
          this.routeLayer = L.polyline(coords, { color: 'blue' }).addTo(this.map);
          this.map.fitBounds(this.routeLayer.getBounds());
        } else {
          alert("No route found.");
        }

      } catch (err) {
        console.error(err);
        alert("Failed to get route.");
      }
    },
    async geocode(address) {
      const key = "d1ab6ff6-8d5b-4ae6-99a6-d80e046f9826"; // same as routing key
      const url = `https://graphhopper.com/api/1/geocode?q=${encodeURIComponent(address)}&limit=1&key=${key}`;
      const res = await fetch(url);
      const data = await res.json();
      if (data.hits && data.hits.length > 0) {
        return [data.hits[0].point.lat, data.hits[0].point.lng]; // [lat, lng]
      } else {
        throw new Error("Address not found: " + address);
      }
    }
  }
};

</script>

<style scoped>
.route-map {
  padding: 40px 20px;
  max-width: 800px;
  margin: auto;
  background: #f8f9fa;
  border-radius: 8px;
}

.input-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  margin-top: 10px;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.result {
  margin-top: 20px;
}

.map {
  height: 400px;
  margin-top: 30px;
  border-radius: 8px;
}
</style>
