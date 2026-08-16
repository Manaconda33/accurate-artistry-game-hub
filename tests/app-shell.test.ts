import { describe, expect, it } from 'vitest';
import { APP_TITLE, mountAppShell } from '../src/app/mountAppShell';

describe('Slice 0 app shell', () => {
  it('mounts the product title without entering gameplay', () => {
    const root = document.createElement('div');

    mountAppShell(root);

    expect(root.querySelector('h1')?.textContent).toBe(APP_TITLE);
    expect(root.textContent).toContain('Enter the Hub');
    expect(root.querySelector('canvas')).toBeNull();
  });
});
