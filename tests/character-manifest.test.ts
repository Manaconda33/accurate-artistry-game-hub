import { describe, expect, it } from 'vitest';
import {
  characterById,
  characterManifest,
  LAVI_ASSET_REVISION,
  MANACONDA_ASSET_REVISION,
  statValues,
  STAT_TOTAL,
  validateCharacterManifest,
} from '../src/characters/manifest';

describe('character manifest', () => {
  it('contains exactly twelve unique, valid profiles', () => {
    expect(validateCharacterManifest()).toEqual([]);
    expect(characterManifest).toHaveLength(12);
    expect(new Set(characterManifest.map(({ id }) => id)).size).toBe(12);
  });

  it('maps Manaconda to the approved production package and AA-09 profile', () => {
    const manaconda = characterById('aa-09');
    expect(manaconda.displayName).toBe('Manaconda');
    expect(manaconda.assetState).toBe('production');
    expect(manaconda.kart).toContain(
      `/assets/characters/aa-09/kart.glb?v=${MANACONDA_ASSET_REVISION}`,
    );
    expect(manaconda.kartVisualYaw).toBe(0);
    expect(manaconda.driver?.rear).toContain(`?v=${MANACONDA_ASSET_REVISION}`);
    expect(manaconda.driver?.steerLeft).toContain(`?v=${MANACONDA_ASSET_REVISION}`);
    expect(manaconda.driver?.steerRight).toContain(`?v=${MANACONDA_ASSET_REVISION}`);
    expect(manaconda.driver?.hit).toContain(`?v=${MANACONDA_ASSET_REVISION}`);
    expect(manaconda.driver?.victory).toContain(`?v=${MANACONDA_ASSET_REVISION}`);
    expect(manaconda.stats).toEqual({
      speed: 7,
      acceleration: 6,
      weight: 6,
      handling: 6,
      miniTurbo: 6,
      traction: 5,
    });
  });

  it.each(characterManifest.map((character) => [character.id, character.stats] as const))(
    '%s totals 36',
    (_id, stats) => {
      expect(statValues(stats).reduce((sum, value) => sum + value, 0)).toBe(STAT_TOTAL);
    },
  );

  it('maps Lavi to the approved production package and profile', () => {
    const lavi = characterById('aa-02');
    expect(lavi.displayName).toBe('Lavi');
    expect(lavi.assetState).toBe('production');
    expect(lavi.kart).toContain(`/assets/characters/aa-02/kart.glb?v=${LAVI_ASSET_REVISION}`);
    expect(lavi.driver?.steerLeft).toContain(`?v=${LAVI_ASSET_REVISION}`);
    expect(lavi.driver?.steerRight).toContain(`?v=${LAVI_ASSET_REVISION}`);
    expect(lavi.stats).toEqual({
      speed: 5,
      acceleration: 8,
      weight: 2,
      handling: 9,
      miniTurbo: 8,
      traction: 4,
    });
  });

  it('falls back to Lavi for an unknown selection id', () => {
    expect(characterById('missing').id).toBe('aa-02');
  });
});
