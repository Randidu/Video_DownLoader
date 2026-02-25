import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Output production build into backend/static so FastAPI serves the frontend.
    outDir: resolve(__dirname, '../backend/static'),
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    proxy: {
      // In dev mode, proxy API calls to the FastAPI backend
      '/video': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
      '/debug': 'http://localhost:8000',
    },
  },
});
