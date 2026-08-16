export const APP_TITLE = 'Accurate Artistry Game Hub';

export function mountAppShell(root: HTMLElement): void {
  root.innerHTML = `
    <main class="shell">
      <p class="eyebrow">Slice 0 · Repository &amp; Project Bootstrap</p>
      <h1>${APP_TITLE}</h1>
      <p class="status">Technical foundation verified. Gameplay begins only after Slice 0 approval.</p>
    </main>
  `;
}
