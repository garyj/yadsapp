import { join, resolve } from 'path'
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import FullReload from 'vite-plugin-full-reload'

const INPUT_DIR = resolve(__dirname, './src/frontend')
const OUTPUT_DIR = resolve(__dirname, './static/dist')

export default defineConfig(({ command, mode }) => ({
  root: INPUT_DIR,
  base: '/static/',
  server: {
    allowedHosts: true,
    cors: true,
    host: 'vite', // same as the name of the docker compose service
    hot: true,
    // https://vitejs.dev/guide/performance#warm-up-frequently-used-files
    warmup: {
      clientFiles: [join(INPUT_DIR, 'project.css'), join(INPUT_DIR, 'project.js')]
    }
  },
  resolve: {
    alias: {
      '@': INPUT_DIR,
      '~': resolve(__dirname, 'node_modules')
    }
  },
  plugins: [
    tailwindcss(),
    FullReload('src/**/*.py', { delay: 275 }),
    FullReload('packages/**/*.py', { delay: 275 }) // TODO check if this will work?
  ],
  define: {
    'process.env.NODE_ENV': JSON.stringify(mode)
  },

  build: {
    manifest: true,
    emptyOutDir: true,
    outDir: resolve(OUTPUT_DIR),
    publicDir: resolve(INPUT_DIR, 'public'),
    sourcemap: true,
    rollupOptions: {
      input: {
        'css/project': join(INPUT_DIR, 'project.css'),
        'js/project': join(INPUT_DIR, 'project.js')
      }
    }
  }
}))
