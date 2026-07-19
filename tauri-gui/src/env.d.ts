/// <reference types="vite/client" />

declare module '@lucide/vue' {
  export * from '@lucide/vue/dist/lucide-vue';
}

declare module '*.vue' {
  import type { DefineComponent } from 'vue';
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

