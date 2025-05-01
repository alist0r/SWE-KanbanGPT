import { defineConfig, UserConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    // adds jsdom to vite, jsdom partially implements
    // the web browser API, and emulates enough of a
    // subset of a web browser to be useful for testing
    // and scraping real-world web applications
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setup.js', // tests is in root of project
  }
} as UserConfig)
