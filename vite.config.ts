import { defineConfig } from 'vitest/config';

export default defineConfig({
  base: '/accurate-artistry-game-hub/',
  test: {
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary'],
      reportsDirectory: 'coverage',
    },
  },
});
