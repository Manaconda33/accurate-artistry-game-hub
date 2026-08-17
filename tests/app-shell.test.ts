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

  it('routes Grand Prix through a twelve-slot character selection scaffold', () => {
    const root = document.createElement('div');
    mountAppShell(root);
    root.querySelector<HTMLElement>('[data-action="enter"]')?.click();
    root.querySelector<HTMLElement>('[data-action="play"]')?.click();

    expect(root.querySelectorAll('[data-character]')).toHaveLength(12);
    expect(root.querySelector('[data-character="aa-02"]')?.getAttribute('aria-pressed')).toBe(
      'true',
    );
    expect(root.textContent).toContain('Race as Lavi');

    root.querySelector<HTMLElement>('[data-character="aa-06"]')?.click();
    expect(root.textContent).toContain('Race as AA 06');
    expect(root.textContent).toContain('Fallback prototype');
  });

  it('replaces a failed production portrait with the character monogram', () => {
    const root = document.createElement('div');
    mountAppShell(root);
    root.querySelector<HTMLElement>('[data-action="enter"]')?.click();
    root.querySelector<HTMLElement>('[data-action="play"]')?.click();
    const portrait = root.querySelector<HTMLImageElement>('[data-character="aa-02"] img');
    portrait?.dispatchEvent(new Event('error'));
    expect(root.querySelector('[data-character="aa-02"] .portrait-fallback')?.textContent).toBe(
      'LV',
    );
  });
});
