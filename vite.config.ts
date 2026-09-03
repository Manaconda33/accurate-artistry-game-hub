import { defineConfig } from 'vitest/config';

export default defineConfig({
  base: '/manacondas-minigame-mayhem/',
  test: {
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary'],
      reportsDirectory: 'coverage',
    },
  },
});
