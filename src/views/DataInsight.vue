<template>
  <section class="insight">
    <h1 class="insight__title">Data Insights</h1>

    <!-- Switch -->
    <div class="switch">
      <button
          class="switch__btn"
          :class="{ active: active === 'population' }"
          @click="setActive('population')"
      >Population</button>

      <button
          class="switch__btn"
          :class="{ active: active === 'carparks' }"
          @click="setActive('carparks')"
      >Carparks</button>

      <button
          class="switch__btn"
          :class="{ active: active === 'spaces' }"
          @click="setActive('spaces')"
      >Parking Spaces</button>
    </div>

    <!-- Metric card (animated) -->
    <transition name="pop">
      <div class="metric" :key="active">
        <div class="metric__label">{{ current.title }}</div>
        <div class="metric__value">
          {{ prettyNumber(animatedVal) }}
          <span class="metric__suffix" v-if="current.suffix">{{ current.suffix }}</span>
        </div>
        <div class="metric__sub" v-if="current.subtitle">{{ current.subtitle }}</div>
      </div>
    </transition>

    <!-- Chart -->
    <div class="chart-card">
      <canvas ref="chartEl"></canvas>
    </div>
  </section>
</template>

<script>
import Papa from 'papaparse'
import Chart from 'chart.js/auto'

export default {
  name: 'DataInsight',
  data() {
    return {
      active: 'population',
      animatedVal: 0,

      // headline metrics for the card
      metrics: {
        population: { title: 'Latest Population', value: 0, suffix: '', subtitle: '' },
        carparks:   { title: 'Carparks (yearly total)', value: 0, suffix: '', subtitle: '' },
        spaces:     { title: 'Total Parking Spaces (latest)', value: 0, suffix: '', subtitle: '' },
      },

      // raw rows
      popRows: [],
      carparkRows: [],
      spaceRows: [],

      // prepared time series for charts
      series: {
        population: { labels: [], data: [] },
        carparks:   { labels: [], data: [] },
        spaces:     { labels: [], data: [] },
      },

      chart: null,
      animRAF: null,
    }
  },

  computed: {
    current() {
      return this.metrics[this.active] || { title: '', value: 0, suffix: '', subtitle: '' }
    }
  },

  mounted() {
    this.loadAll()
  },

  methods: {
    /* --------------------- Load & parse --------------------- */
    async loadAll() {
      const base = process.env.BASE_URL || '/'
      const [pop, carparks, spaces] = await Promise.all([
        this.loadCSV(`${base}data/population_yearly.csv`),
        this.loadCSV(`${base}data/cbd_carparks.csv`),
        this.loadCSV(`${base}data/cbd_spaces.csv`),
      ])

      this.popRows = pop
      this.carparkRows = carparks
      this.spaceRows = spaces

      this.buildPopulation()
      this.buildCarparks()
      this.buildSpaces()

      // initial render
      this.setActive(this.active)
    },

    loadCSV(url) {
      return new Promise((resolve) => {
        Papa.parse(url, {
          download: true,
          header: true,
          skipEmptyLines: true,
          complete: (res) => resolve(res.data || []),
          error: () => resolve([]),
        })
      })
    },

    /* --------------------- Helpers --------------------- */
    num(v) {
      if (v == null) return 0
      const n = String(v).replace(/[^0-9.-]/g, '')
      const x = parseFloat(n)
      return Number.isFinite(x) ? x : 0
    },
    findCol(row, regexList, fallback = null) {
      const keys = Object.keys(row || {})
      for (const re of regexList) {
        const hit = keys.find(k => re.test(k))
        if (hit) return hit
      }
      return fallback
    },
    prettyNumber(n) {
      return n.toLocaleString()
    },

    /* --------------------- Series builders --------------------- */
    // Population: year -> population
    buildPopulation() {
      if (!this.popRows.length) return
      const first   = this.popRows[0]
      const yearCol = this.findCol(first, [/^year$/i, /yr/i, /date/i])
      const popCol  = this.findCol(first, [/^population$/i, /pop/i, /people/i])

      if (!yearCol || !popCol) return

      const rows   = [...this.popRows]
          .filter(r => r[yearCol] != null && r[popCol] != null)
          .sort((a, b) => this.num(a[yearCol]) - this.num(b[yearCol]))

      const labels = rows.map(r => String(r[yearCol]))
      const data   = rows.map(r => this.num(r[popCol]))

      this.series.population = { labels, data }
      this.setHeadlineFromSeries('population')
    },

    // Carparks: year -> Carpark_Count (already aggregated in CSV)
    buildCarparks() {
      if (!this.carparkRows.length) return
      const first    = this.carparkRows[0]
      const yearCol  = this.findCol(first, [/^year$/i, /yr/i, /date/i])
      const countCol = this.findCol(first, [/carpark.*count/i, /^count$/i, /total.*carpark/i], 'Carpark_Count')

      if (!yearCol || !countCol) return

      const rows   = [...this.carparkRows]
          .filter(r => r[yearCol] != null && r[countCol] != null)
          .sort((a, b) => this.num(a[yearCol]) - this.num(b[yearCol]))

      const labels = rows.map(r => String(r[yearCol]))
      const data   = rows.map(r => this.num(r[countCol]))

      this.series.carparks = { labels, data }
      this.setHeadlineFromSeries('carparks')
    },

    // Parking spaces: year -> sum of spaces (or Total_Spaces)
    buildSpaces() {
      if (!this.spaceRows.length) return
      const first     = this.spaceRows[0]
      const yearCol   = this.findCol(first, [/^year$/i, /yr/i, /date/i])
      const spacesCol = this.findCol(first, [/^total.*spaces?$/i, /spaces?/i, /capacity/i, /bays?/i], 'Total_Spaces')

      if (!yearCol || !spacesCol) return

      // If your CSV is already aggregated by year, this will just map.
      // If it has multiple rows per year, this reduces them into a sum.
      const totals = new Map()
      this.spaceRows.forEach(r => {
        const y = r[yearCol] != null ? String(r[yearCol]).trim() : ''
        if (!y) return
        const v = this.num(r[spacesCol])
        totals.set(y, (totals.get(y) || 0) + v)
      })

      const labels = Array.from(totals.keys()).sort((a, b) => this.num(a) - this.num(b))
      const data   = labels.map(y => totals.get(y))

      this.series.spaces = { labels, data }
      this.setHeadlineFromSeries('spaces')
    },

    // Compute card headline (latest value + YoY) from a named series
    setHeadlineFromSeries(key) {
      const { labels, data } = this.series[key]
      if (!data.length) return
      const len  = data.length
      const last = data[len - 1] || 0
      const prev = data[len - 2] || 0
      const yoy  = prev ? ((last - prev) / prev) * 100 : 0

      this.metrics[key].value    = last
      this.metrics[key].subtitle = prev
          ? `YoY change: ${yoy.toFixed(1)}% (${labels[len - 2]}→${labels[len - 1]})`
          : 'No previous year'
    },

    /* --------------------- UI & Chart --------------------- */
    setActive(key) {
      this.active = key
      // animate number
      this.animateTo(this.metrics[key].value || 0)
      // update chart
      this.renderChartFor(key)
    },

    animateTo(target) {
      if (this.animRAF) cancelAnimationFrame(this.animRAF)
      const startVal = this.animatedVal || 0
      const start = performance.now()
      const duration = 700
      const step = (t) => {
        const p = Math.min(1, (t - start) / duration)
        const eased = 1 - Math.pow(1 - p, 3) // easeOutCubic
        this.animatedVal = Math.round(startVal + (target - startVal) * eased)
        if (p < 1) this.animRAF = requestAnimationFrame(step)
      }
      this.animRAF = requestAnimationFrame(step)
    },

    renderChartFor(key) {
      const ctx = this.$refs.chartEl.getContext('2d')
      const s = this.series[key] || { labels: [], data: [] }

      const config = {
        type: 'line',
        data: {
          labels: s.labels,
          datasets: [{
            data: s.data,
            borderWidth: 2,
            fill: true,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { mode: 'index', intersect: false }
          },
          scales: {
            x: { ticks: { color: '#cfd6e4' }, grid: { color: 'rgba(255,255,255,.06)' } },
            y: { beginAtZero: true, ticks: { color: '#cfd6e4' }, grid: { color: 'rgba(255,255,255,.06)' }}
          }
        }
      }

      if (this.chart) {
        this.chart.data = config.data
        this.chart.options = config.options
        this.chart.update()
      } else {
        this.chart = new Chart(ctx, config)
      }
    },
  },

  beforeDestroy() {
    if (this.animRAF) cancelAnimationFrame(this.animRAF)
    if (this.chart) this.chart.destroy()
  },
}
</script>

<style scoped>
.insight {
  display: flex;
  flex-direction: column;
  max-width: 90vw;
  max-height: 80vh;
  margin: 24px auto;
  padding: 16px;
  color: #e9edf4;
}
.insight__title {
  font-size: 32px;
  font-weight: 800;
  margin: 0 0 16px;
}

/* Switch */
.switch {
  display: inline-flex;
  background: #161a22;
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 999px;
  padding: 4px;
  gap: 4px;
}
.switch__btn {
  background: transparent;
  color: #cfd6e4;
  border: 0;
  padding: 8px 14px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 600;
}
.switch__btn.active {
  background: linear-gradient(135deg, #4ca3ff, #7b7bff);
  color: #0c111a;
}

/* Metric card */
.metric {
  margin-top: 14px;
  background: #1a1f2a;
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,.25);
}
.metric__label { font-size: 14px; color: #aeb8cc; margin-bottom: 6px; }
.metric__value { font-size: 48px; font-weight: 900; line-height: 1.1; }
.metric__suffix { font-size: 20px; font-weight: 700; margin-left: 6px; color: #aeb8cc; }
.metric__sub   { margin-top: 6px; color: #aeb8cc; }

/* Chart card */
.chart-card {
  margin-top: 14px;
  background: #161b25;
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 16px;
  height: 60vh;
  padding: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,.22);
}

@media (max-width: 768px) {
  .insight {
    max-width: 100%;
    padding: 12px;
  }
  .chart-card {
    height: 50vh;
  }
}

/* Pop animation for metric */
.pop-enter-active {
  transition: opacity .25s ease, transform .25s ease, filter .25s ease;
}
.pop-enter {
  opacity: 0;
  transform: translateY(6px) scale(.98);
  filter: blur(2px);
}
</style>
