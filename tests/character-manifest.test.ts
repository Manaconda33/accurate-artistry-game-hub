import { describe, expect, it } from 'vitest';
import {
  ACCU_ASSET_REVISION,
  characterById,
  characterManifest,
  LAVI_ASSET_REVISION,
  KRAKEN_ASSET_REVISION,
  MANACONDA_ASSET_REVISION,
  NEGATIVE_Z_KART_VISUAL_YAW,
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
    expect(manaconda.kartVisualYaw).toBe(NEGATIVE_Z_KART_VISUAL_YAW);
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

  it('maps Accu to Pink Precision and the approved AA-11 profile', () => {
    const accu = characterById('aa-11');
    expect(accu.displayName).toBe('Accu');
    expect(accu.descriptor).toBe('Perfect aim. Maximum armor.');
    expect(accu.assetState).toBe('production');
    expect(accu.kart).toContain(`/assets/characters/aa-11/kart.glb?v=${ACCU_ASSET_REVISION}`);
    expect(accu.kartVisualYaw).toBe(NEGATIVE_Z_KART_VISUAL_YAW);
    expect(accu.driver?.rear).toContain(`?v=${ACCU_ASSET_REVISION}`);
    expect(accu.driver?.steerLeft).toContain(`?v=${ACCU_ASSET_REVISION}`);
    expect(accu.driver?.steerRight).toContain(`?v=${ACCU_ASSET_REVISION}`);
    expect(accu.driver?.hit).toContain(`?v=${ACCU_ASSET_REVISION}`);
    expect(accu.driver?.victory).toContain(`?v=${ACCU_ASSET_REVISION}`);
    expect(accu.stats).toEqual({
      speed: 8,
      acceleration: 4,
      weight: 10,
      handling: 3,
      miniTurbo: 5,
      traction: 6,
    });
  });

  it('maps Kraken to The Abyssal Drifter and the approved AA-05 profile', () => {
    const kraken = characterById('aa-05');
    expect(kraken.displayName).toBe('Kraken');
    expect(kraken.descriptor).toBe('Drift Specialist');
    expect(kraken.assetState).toBe('production');
    expect(kraken.kart).toContain(`/assets/characters/aa-05/kart.glb?v=${KRAKEN_ASSET_REVISION}`);
    expect(kraken.kartVisualYaw).toBe(NEGATIVE_Z_KART_VISUAL_YAW);
    expect(kraken.driver?.rear).toContain(`?v=${KRAKEN_ASSET_REVISION}`);
    expect(kraken.driver?.front).toContain(`?v=${KRAKEN_ASSET_REVISION}`);
    expect(kraken.driver?.steerLeft).toContain(`?v=${KRAKEN_ASSET_REVISION}`);
    expect(kraken.driver?.steerRight).toContain(`?v=${KRAKEN_ASSET_REVISION}`);
    expect(kraken.driver?.hit).toContain(`?v=${KRAKEN_ASSET_REVISION}`);
    expect(kraken.driver?.victory).toContain(`?v=${KRAKEN_ASSET_REVISION}`);
    expect(kraken.stats).toEqual({
      speed: 6,
      acceleration: 7,
      weight: 5,
      handling: 6,
      miniTurbo: 9,
      traction: 3,
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

  it('rejects a production kart that bypasses the enforced orientation contract', () => {
    const invalid = characterManifest.map((character) =>
      character.id === 'aa-11' ? { ...character, kartVisualYaw: 0 } : character,
    );
    expect(validateCharacterManifest(invalid)).toContain(
      'aa-11 production kart must use the enforced negative-Z visual yaw.',
    );
  });
});
