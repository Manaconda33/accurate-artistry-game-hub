import { Howler } from 'howler';
import type { HudState, KartTimeTrial as KartTimeTrialInstance } from '../game/KartTimeTrial';

export const APP_TITLE = 'Accurate Artistry Game Hub';

function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds - minutes * 60;
  return `${String(minutes)}:${remainder.toFixed(2).padStart(5, '0')}`;
}

function button(label: string, action: string, className = ''): string {
  return `<button class="menu-button ${className}" data-action="${action}">${label}</button>`;
}

export function mountAppShell(root: HTMLElement): void {
  let game: KartTimeTrialInstance | null = null;

  const unlockAudio = async (): Promise<void> => {
    if (Howler.ctx.state === 'suspended') await Howler.ctx.resume();
  };

  const renderTitle = (): void => {
    root.innerHTML = `
      <main class="screen title-screen">
        <div class="title-mark">AA</div>
        <p class="eyebrow">Accurate Artistry presents</p>
        <h1>${APP_TITLE}</h1>
        <p class="lead">A modular arcade playground. Slice 1 time trial is ready.</p>
        ${button('Enter the Hub', 'enter', 'primary')}
        <p class="microcopy">Press or click to unlock browser audio.</p>
      </main>`;
  };

  const renderMenu = (): void => {
    root.innerHTML = `
      <main class="screen menu-screen">
        <header><p class="eyebrow">Game Hub</p><h1>Choose an experience</h1></header>
        <section class="game-grid">
          <article class="game-card playable">
            <span class="card-tag">Slice 1 playable</span>
            <h2>Circuit Alpha Time Trial</h2>
            <p>Three laps. One kart. Ordered checkpoints. Pure keyboard control.</p>
            ${button('Start Time Trial', 'play', 'primary')}
          </article>
          <article class="game-card unavailable" aria-disabled="true">
            <span class="card-tag">Future game</span><h2>Gallery Gauntlet</h2><p>Unavailable in this build.</p>
          </article>
          <article class="game-card unavailable" aria-disabled="true">
            <span class="card-tag">Future game</span><h2>Inkstorm Arena</h2><p>Unavailable in this build.</p>
          </article>
        </section>
        <nav class="utility-nav">${button('Controls', 'controls')}${button('Settings', 'settings')}</nav>
      </main>`;
  };

  const renderControls = (): void => {
    root.innerHTML = `
      <main class="screen compact-screen"><p class="eyebrow">Reference</p><h1>Controls</h1>
        <dl class="control-list">
          <div><dt>Accelerate</dt><dd>W / ↑</dd></div><div><dt>Brake &amp; reverse</dt><dd>S / ↓</dd></div>
          <div><dt>Steer</dt><dd>A D / ← →</dd></div><div><dt>Hop / drift</dt><dd>Space + steer</dd></div>
          <div><dt>Rear camera</dt><dd>C</dd></div><div><dt>Recover kart</dt><dd>R</dd></div>
          <div><dt>Pause</dt><dd>Esc / P</dd></div>
        </dl>${button('Back', 'menu', 'primary')}</main>`;
  };

  const renderSettings = (): void => {
    root.innerHTML = `
      <main class="screen compact-screen"><p class="eyebrow">Local settings</p><h1>Settings</h1>
        <label class="setting"><span>Master volume</span><input id="volume" type="range" min="0" max="1" step="0.05" value="${String(Howler.volume())}" /></label>
        <p class="lead small">Visual quality adapts to the browser in this foundational slice.</p>
        ${button('Back', 'menu', 'primary')}</main>`;
    const volume = root.querySelector<HTMLInputElement>('#volume');
    if (volume !== null) {
      volume.addEventListener('input', (event) => {
        Howler.volume(Number((event.target as HTMLInputElement).value));
      });
    }
  };

  const renderGame = async (): Promise<void> => {
    root.innerHTML = `
      <section class="game-shell" aria-label="Circuit Alpha time trial">
        <canvas id="game-canvas" tabindex="0"></canvas>
        <div class="hud top-left"><span>Lap</span><strong id="lap">1 / 3</strong></div>
        <div class="hud top-center"><span>Time</span><strong id="time">0:00.00</strong></div>
        <div class="hud top-right"><span>Speed</span><strong id="speed">0 km/h</strong></div>
        <div class="hud bottom-left"><span>Surface</span><strong id="surface">ASPHALT</strong></div>
        <div class="hud bottom-right performance"><span>Performance</span><strong id="performance">60 FPS · 16.7 ms</strong></div>
        <div id="drift-panel" class="drift-panel" data-tier="none">
          <span id="drift-label">Hold Space + steer to drift</span>
          <div class="drift-meter"><i id="drift-fill"></i></div>
        </div>
        <div id="wrong-way" class="warning" hidden>WRONG WAY</div>
        <div id="loading" class="loading-card"><span class="spinner"></span><h2>Initializing Circuit Alpha</h2><p>Loading Rapier physics and the procedural track…</p></div>
        <div id="finish" class="finish-card" hidden><p class="eyebrow">Time trial complete</p><h2 id="finish-time">0:00.00</h2>${button('Return to Hub', 'finish-menu', 'primary')}</div>
        <div class="game-help">WASD / arrows drive · Space + steer drift · C rear view · R recover · Esc pause</div>
      </section>`;

    const canvas = root.querySelector<HTMLCanvasElement>('#game-canvas');
    if (canvas === null) throw new Error('Game canvas was not created.');
    const { KartTimeTrial } = await import('../game/KartTimeTrial');
    const getElement = (selector: string): HTMLElement => {
      const element = root.querySelector<HTMLElement>(selector);
      if (element === null) throw new Error(`Required UI element missing: ${selector}`);
      return element;
    };
    const updateHud = (state: HudState): void => {
      getElement('#lap').textContent = `${String(state.lap)} / 3`;
      getElement('#time').textContent = formatTime(state.elapsed);
      getElement('#speed').textContent = `${String(state.speedKph)} km/h`;
      getElement('#surface').textContent = state.surface.toUpperCase();
      getElement('#performance').textContent =
        `${String(state.fps)} FPS · ${state.frameMs.toFixed(1)} ms`;
      getElement('#wrong-way').hidden = !state.wrongWay;
      const driftPanel = getElement('#drift-panel');
      driftPanel.dataset.tier = state.driftTier;
      getElement('#drift-fill').style.width = `${String(Math.round(state.driftCharge * 100))}%`;
      getElement('#drift-label').textContent = state.airborne
        ? 'AIRBORNE'
        : state.boostActive
          ? `${state.driftTier.toUpperCase()} BOOST`
          : state.driftTier === 'none'
            ? 'Hold Space + steer to drift'
            : `${state.driftTier.toUpperCase()} CHARGE`;
    };
    game = await KartTimeTrial.create({
      canvas,
      onHud: updateHud,
      onFinish: (time) => {
        getElement('#finish').hidden = false;
        getElement('#finish-time').textContent = formatTime(time);
      },
    });
    const loading = root.querySelector('#loading');
    if (loading !== null) loading.remove();
    canvas.focus();
    game.start();
  };

  root.addEventListener('click', (event) => {
    const target = (event.target as HTMLElement).closest<HTMLElement>('[data-action]');
    if (target === null) return;
    const action = target.dataset.action;
    void unlockAudio();
    if (action === 'enter' || action === 'menu') renderMenu();
    if (action === 'controls') renderControls();
    if (action === 'settings') renderSettings();
    if (action === 'play') void renderGame();
    if (action === 'finish-menu') {
      game?.dispose();
      game = null;
      renderMenu();
    }
  });

  renderTitle();
}
