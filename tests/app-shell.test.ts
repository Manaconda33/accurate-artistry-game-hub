import { describe, expect, it } from 'vitest';
import { APP_TITLE, mountAppShell } from '../src/app/mountAppShell';

describe('Slice 0 app shell', () => {
  it('mounts the product title and Slice 0 boundary', () => {
    const root = document.createElement('div');

    mountAppShell(root);

    expect(root.querySelector('h1')?.textContent).toBe(APP_TITLE);
    expect(root.textContent).toContain('Slice 0');
    expect(root.textContent).toContain('Gameplay begins only after Slice 0 approval.');
  });
});
