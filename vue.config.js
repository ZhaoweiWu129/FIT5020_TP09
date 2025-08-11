const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080, // Vue dev server
    proxy: {
      // forward API calls to the backend
      '^/(parking|stations|park_ride)': {
        target: process.env.VUE_APP_API_BASE || 'http://localhost:8000/',
        changeOrigin: true,
      },
    },
  },
});
