import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import tailwind from '@tailwindcss/vite';
export default defineConfig({plugins:[react(),tailwind()],build:{rollupOptions:{output:{manualChunks:{graph:['cytoscape'],ui:['@radix-ui/react-dialog','@tanstack/react-query']}}}},server:{proxy:{'/api':'http://127.0.0.1:8766'}}});
