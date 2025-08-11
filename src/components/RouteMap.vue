<script setup>
import { onMounted, nextTick, ref } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
//api for https
// const API_BASE = process.env.VUE_APP_API_BASE || '';

//Icon URLs and markers
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import trainPng from '@/assets/train.png';
import parkPng from '@/assets/parking-meter-export.png';
import ParkRide from '@/assets/parkandride.png';
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});
const stationIcon = L.icon({
  iconUrl: trainPng
});
const ParkIcon = L.icon({
  iconUrl: parkPng
});
const ParkRideIcon = L.icon({
  iconUrl: ParkRide
});


const start = ref('Boxhill, Melbourne');
const end   = ref('Flinders Street, Melbourne');
const summary = ref(null);
const mapEl = ref(null);
//list for stored
const stationsList = ref([]);
const parkRideList = ref([]);
const parkingList = ref([]);

let map, routeLayer, markers = [];
let stationLayer;
let parkRideLayer;
let destParkingLayer;
const maxDistanceStations = ref(600)
const maxDistanceParkRide = ref(800)
const maxDistanceParking = ref(600)

onMounted(async () => {
  await nextTick();
  map = L.map(mapEl.value).setView([-37.8136, 144.9631], 14);
  //Layers
  parkRideLayer = L.layerGroup().addTo(map);
  stationLayer = L.layerGroup().addTo(map);
  destParkingLayer = L.layerGroup().addTo(map);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
  }).addTo(map);
  setTimeout(() => map.invalidateSize(), 0);
  window.addEventListener('resize', () => map.invalidateSize());
});

async function geocode(address) {
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1&addressdetails=0`;
  const res = await fetch(url, { headers: { 'Accept-Language': 'en' } });
  if (!res.ok) throw new Error(`Geocode failed: ${res.status}`);
  const data = await res.json();
  if (!data.length) throw new Error(`No match for: ${address}`);
  const { lat, lon, name, display_name } = data[0];
  // NOTE: OSRM expects lon,lat order
  const display_name_ = display_name.split(',').slice(0, 3).join(', ');
  return [parseFloat(lon), parseFloat(lat), name == '' ? display_name_ : name];
}

function sampleRoutePoints(lngLatCoords, maxSamples = 20, stride = 12) {
  const picked = [];
  for (let i = 0; i < lngLatCoords.length; i += stride) {
    picked.push(lngLatCoords[i]);
    if (picked.length >= maxSamples) break;
  }
  if (lngLatCoords.length && picked[picked.length - 1] !== lngLatCoords[lngLatCoords.length - 1]) {
    picked.push(lngLatCoords[lngLatCoords.length - 1]);
  }
  return picked;
}

//Fetch Station along route
async function fetchStationsAlongRouteFrontend(lngLatCoords, maxdistance = 600) {
  if (!lngLatCoords?.length) return;
  if (!stationLayer) stationLayer = L.layerGroup().addTo(map);

  const samples = sampleRoutePoints(lngLatCoords, 20, 12);
  const byId = new Map();
  const batchSize = 5;

  for (let i = 0; i < samples.length; i += batchSize) {
    const batch = samples.slice(i, i + batchSize);
    // Build the stations list from the merged results
    stationsList.value = Array.from(byId.values());

    const calls = batch.map(([lng, lat]) =>
        //Fetch from backend py file near start location function
        fetch(`/stations/near_location`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            maxdistance,
            coordinates: { lat, long: lng }
          })
        })
            .then(r => r.ok ? r.json() : { stations: [] })
            .catch(() => ({ stations: [] }))
    );

    const results = await Promise.all(calls);


    results.forEach(({ stations }) => {
      stations.forEach(s => {
        const prev = byId.get(s.id);
        if (!prev || s.distance_m < prev.distance_m) byId.set(s.id, s);
      });
    });
  }

  stationLayer.clearLayers();
  Array.from(byId.values()).forEach(s => {
    //Marker for station
    L.marker([s.location.lat, s.location.long],{icon:stationIcon})
        .bindPopup(`${s.name}<br>${Math.round(s.distance_m)} m from route`)
        .addTo(stationLayer);
  });
}
async function fetchParkRideAlongRoute(rawLngLatCoords, maxdistance = 800) {
  if (!rawLngLatCoords?.length) return;
  if (!parkRideLayer) parkRideLayer = L.layerGroup().addTo(map);
  if (!stationLayer) stationLayer = L.layerGroup().addTo(map);

  //Fetch from backend py file park and ride function
  const res = await fetch(`/park_ride`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      maxdistance,
      coordinates: rawLngLatCoords // IMPORTANT: [lng,lat] as returned by OSRM
    })
  });
  if (!res.ok) { console.warn('park_ride failed'); return; }
  const data = await res.json(); // { park_and_ride: [...] }
  parkRideList.value = data.park_and_ride || []


  parkRideLayer.clearLayers();
  (data.park_and_ride || []).forEach(p => {
    // backend returns centroid as "parking_area_centroid" (it is the polygon centroid)
    const { lat, long } = p.parking_area_centroid;
    //marker for parkRide
    L.marker([lat, long],{icon:ParkRideIcon})
        //Park and ride marker
        .bindPopup(
            `<b>${p.zone_name ?? 'Park & Ride'}</b><br>
         Nearest station: ${p.nearest_train_station_name}<br>
         ~${Math.round(p.distance_m)} m from route`
        )
        .addTo(parkRideLayer);
    // Add station marker if it exists
    L.marker([p.nearest_train_station_coords.lat, p.nearest_train_station_coords.long],{icon:stationIcon})
        .bindPopup(`Station: ${p.nearest_train_station_name}<br>${Math.round(p.ts_pr_distance_m)} m from park & ride`)
        .addTo(stationLayer);
  });
}
async function fetchParkingNearPoint(lat, lng, maxdistance = 600) {
  if (!destParkingLayer) destParkingLayer = L.layerGroup().addTo(map);

  const res = await fetch(`/parking/near_location`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      maxdistance,
      coordinates: { lat, long: lng }
    })
  });
  if (!res.ok) { console.warn('parking near dest failed'); return; }

  const data = await res.json(); // array of parkings

  parkingList.value = data;
  destParkingLayer.clearLayers();
  data.forEach(p => {
    const { lat: cenLat, long: cenLng } = p.parking_area_centroid;
    L.marker([cenLat, cenLng],{icon:ParkIcon})
        .bindPopup(`${p.name ?? 'Parking'} - ${Math.round(p.distance_meters)} m from destination`)
        .addTo(destParkingLayer);
  });
}


async function getRoute() {
  try {
    clearRoute();
    const [fromLonLat, toLonLat] = await Promise.all([
      geocode(start.value),
      geocode(end.value),
    ]);

    const osrmUrl =
        `https://router.project-osrm.org/route/v1/driving/` +
        `${fromLonLat[0]},${fromLonLat[1]};${toLonLat[0]},${toLonLat[1]}` +
        `?overview=full&geometries=geojson&steps=false&annotations=false`;

    const res = await fetch(osrmUrl);
    if (!res.ok) throw new Error(`OSRM failed: ${res.status}`);
    const json = await res.json();
    if (json.code !== 'Ok' || !json.routes?.length) throw new Error('No route returned');

    const route = json.routes[0];
    const coords = route.geometry.coordinates.map(([lon, lat]) => [lat, lon]); // Leaflet wants lat,lng
    routeLayer = L.polyline(coords, { weight: 5, opacity: 0.9 }).addTo(map);

    //Fetch nearest station
    const routeData = json.routes[0];

    // For backend fetch (lng,lat as OSRM gives them)
    const rawCoords = routeData.geometry.coordinates;
    //Distance fetch within range
    await fetchStationsAlongRouteFrontend(rawCoords, maxDistanceStations.value)
    await fetchParkRideAlongRoute(rawCoords, maxDistanceParkRide.value)
    await fetchParkingNearPoint(toLonLat[1], toLonLat[0], maxDistanceParking.value)


    // Markers
    markers.push(L.marker([fromLonLat[1], fromLonLat[0]]).bindPopup(`Starting Location: ${fromLonLat[2]}`).addTo(map));
    markers.push(L.marker([toLonLat[1], toLonLat[0]]).bindPopup(`Destination: ${toLonLat[2]}`).addTo(map));

    map.fitBounds(routeLayer.getBounds(), { padding: [24, 24] });
    // Call backend: find parking near the start point of the route first function from
    // try {
    //   const startLatLng = coords[0]; // coords is [[lat, lng], ...]
    //   const res = await fetch('/parking/near_location', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({
    //       maxdistance: maxDistance.value, // meters
    //       coordinates: { lat: startLatLng[0], long: startLatLng[1] }
    //     }),
    //   });
    //   const parkingData = await res.json();

    //   parkingData.forEach(p => {
    //     const { lat, long } = p.parking_area_centroid;
    //     L.marker([lat, long])
    //         .addTo(map)
    //         .bindPopup(`${p.name || 'Parking'} - ${Math.round(p.parking_to_station_meters)} m`);
    //   });
    // } catch (err) {
    //   console.error('Error fetching parking:', err);
    // }

    //show summary
    summary.value = {
      distance: `${Math.round(route.distance / 1000)} km`,
      duration: `${Math.round(route.duration / 60)} min`,
    };


  } catch (e) {
    console.error(e);
    alert(e.message);
  }
}

function clearRoute() {
  if (routeLayer) { map.removeLayer(routeLayer); routeLayer = null; }
  markers.forEach(m => map.removeLayer(m));
  markers = [];
  summary.value = null;
}

</script>

<template>
  <section class="route">
    <h1 class="route__title">Find a Route</h1>
    <div class="route__grid">
      <form class="card route__form" @submit.prevent="getRoute">
        <label class="field">
          <span class="field__label">Start</span>
          <input class="field__input" v-model="start" placeholder="Flinders Street, Melbourne" />
        </label>
        <label class="field">
          <span class="field__label">Destination</span>
          <input class="field__input" v-model="end" placeholder="Russell Street, Melbourne" />
        </label>
        <div class="summary" v-if="summary">
          <div class="summary__pill">Time: {{ summary.duration }}  Distance: {{ summary.distance }}</div>
        </div>
        <hr />
        <label>Display Filters</label>
        <label>Max. distance of stations from your route: {{ maxDistanceStations }}m</label>
        <input type="range" min="100" max="2000" step="50" v-model="maxDistanceStations" />

        <label>Max. distance of Park & Ride zones from your route: {{ maxDistanceParkRide }}m</label>
        <input type="range" min="100" max="2000" step="50" v-model="maxDistanceParkRide" />

        <label>Max. distance of public parking spaces from your destination: {{ maxDistanceParking }}m</label>
        <input type="range" min="100" max="2000" step="50" v-model="maxDistanceParking" />

        <div class="actions">
          <button class="btn btn--primary" type="submit">Get Route</button>
        </div>
      </form>

      <div class="card route__map">
        <div id="map" ref="mapEl"></div>
      </div>

      <!-- Stations -->
      <template v-if="stationsList.length">
        <h3>Stations</h3>
        <div class="scroll-list">
          <ul>
            <li v-for="(s,i) in stationsList" :key="s.id || s['@id'] || i">
              {{ s.name || 'Station' }} ({{ Math.round(s.distance_m) }}m from route)
            </li>
          </ul>
        </div>
      </template>

      <!-- Park & Ride -->
      <template v-if="parkRideList && parkRideList.length">
        <h3>Park & Ride</h3>
        <div class="scroll-list">
          <ul>
            <li v-for="(p,i) in parkRideList" :key="p.id || p.zone_id || i">
              {{ p.zone_name || p.name || ('Near ' + (p.nearest_train_station_name || 'station')) }}
            </li>
          </ul>
        </div>
      </template>

      <!-- Public Parking -->
      <template v-if="parkingList && parkingList.length">
        <h3>Public Parking Near Destination</h3>
        <div class="scroll-list">
          <ul>
            <li v-for="(p,i) in parkingList" :key="p.id || i">
              {{ p.name || 'Parking' }} ({{ Math.round(p.distance_meters) }}m from destination)
            </li>
          </ul>
        </div>
      </template>

    </div>
  </section>
</template>

<style scoped>
:root { --bg: #f7f7fb; --card: #ffffff; --ink: #1f2937; --muted:#6b7280; --brand: #02a2ff; --brand-700:#2563eb; }

.route {
  max-width: 1100px;
  margin: 24px auto;
  padding: 16px;
}
.route__title {
  font-size: 24px;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 16px;
  letter-spacing: .2px;
}
.route__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* .route__grid {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 16px;
  align-items: start;
} */

.scroll-list {
  max-height: 180px;
  overflow-y: auto;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 16px;
  padding: 6px 0;
  border: 1px solid #e5e7eb;
}
.scroll-list ul {
  margin: 0;
  padding: 0 12px;
  list-style: none;
}
.scroll-list li {
  padding: 6px 0;
  border-bottom: 1px solid #f3f4f6;
  font-size: 14px;
}
.scroll-list li:last-child {
  border-bottom: none;
}

@media (min-width: 960px) {
  .route__grid { grid-template-columns: 380px 1fr; }
}

.card {
  background: var(--card);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,.06);
  border: 1px solid rgba(17,24,39,.06);
}
.route__form {
  display: flex;
  flex-direction: column;
  justify-content: center;  /* center vertically */
  align-items: stretch;     /* make inputs/button full width */
  height: 100%;
  padding: 24px;            /* consistent inner padding */
  box-sizing: border-box;
  gap: 12px;                 /* equal spacing between fields/buttons */
}
.route__map { padding: 12px; }

.field { display: grid; gap: 6px; margin-bottom: 12px; }
.field__label { font-size: 13px; color: var(--muted); }
.field__input {
  height: 42px; padding: 0 12px; border-radius: 10px;
  border: 1px solid rgba(17,24,39,.12); outline: none; font-size: 14px;
}
.field__input:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 4px rgba(59,130,246,.15);
}

.actions {
  margin-top: 0;        /* space above button */
}
.btn {
  height: 42px;
  padding: 0 16px;
  border-radius: 10px;
  border: 0;
  cursor: pointer;
  font-weight: 600;
  color: #616975;
}
.btn--primary {
  background: linear-gradient(180deg, #3b82f6, #0048e8);
  color: #fff;
  height: 42px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}
.btn--primary:hover { filter: brightness(.98); transform: translateY(-1px); }

.summary { margin-top: 10px; }
.summary__pill {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  background: #f3f4f6;
  font-size: 13px;
  font-weight: 600;
  color: #111827;
}


#map {
  width: 100%;
  height: 520px;              /* taller, feels premium */
  border-radius: 12px;
  overflow: hidden;
}

</style>
