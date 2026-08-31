import { describe, expect, it } from 'vitest';
import {
  ACCU_ASSET_REVISION,
  archivedCleo,
  characterById,
  characterManifest,
  LAVI_ASSET_REVISION,
  KRAKEN_ASSET_REVISION,
  KEEG_ASSET_REVISION,
  KRIOS_ASSET_REVISION,
  MANACONDA_ASSET_REVISION,
  MCFLEURDEL_ASSET_REVISION,
  TOPH_ASSET_REVISION,
  LULA_ASSET_REVISION,
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
    expect(manaconda.frontDriverSpritePosition).toEqual([0, 0.45, -0.12]);
    expect(manaconda.driver?.rear).toContain(`?v=${MANACONDA_ASSET_REVISION}`);
    expect(manaconda.driver?.front).toContain(`?v=${MANACONDA_ASSET_REVISION}`);
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
    expect(accu.driverSpritePosition).toEqual([0, 0.55, 0.55]);
    expect(accu.frontDriverSpritePosition).toEqual([0, 0.45, 0.55]);
    expect(accu.driver?.rear).toContain(`?v=${ACCU_ASSET_REVISION}`);
    expect(accu.driver?.front).toContain(`?v=${ACCU_ASSET_REVISION}`);
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

  it('keeps Cleo archived but removes her from the active roster', () => {
    const aa06 = characterById('aa-06');
    expect(aa06.displayName).toBe('AA 06');
    expect(aa06.assetState).toBe('placeholder');
    expect(aa06.portrait).toBeUndefined();
    expect(aa06.kart).toBeUndefined();
    expect(aa06.driver).toBeUndefined();
    expect(characterManifest.some(({ displayName }) => displayName === 'Cleo')).toBe(false);

    expect(archivedCleo.displayName).toBe('Cleo');
    expect(archivedCleo.assetState).toBe('production');
    expect(archivedCleo.kart).toContain('/assets/characters/aa-06/kart.glb');
    expect(archivedCleo.driverSpritePosition).toEqual([0, 0.9, -0.72]);
    expect(archivedCleo.driver?.front).toContain('/assets/characters/aa-06/driver/front.png');
    expect(archivedCleo.driver?.victory).toContain('/assets/characters/aa-06/driver/victory.png');
  });

  it('maps Krios to The Hornbreaker and the approved AA-10 profile', () => {
    const krios = characterById('aa-10');
    expect(krios.displayName).toBe('Krios');
    expect(krios.descriptor).toBe('Straight-Line Heavy');
    expect(krios.assetState).toBe('production');
    expect(krios.kart).toContain(`/assets/characters/aa-10/kart.glb?v=${KRIOS_ASSET_REVISION}`);
    expect(krios.kartVisualYaw).toBe(NEGATIVE_Z_KART_VISUAL_YAW);
    expect(krios.driver?.rear).toContain(`?v=${KRIOS_ASSET_REVISION}`);
    expect(krios.driver?.front).toContain(`?v=${KRIOS_ASSET_REVISION}`);
    expect(krios.driver?.steerLeft).toContain(`?v=${KRIOS_ASSET_REVISION}`);
    expect(krios.driver?.steerRight).toContain(`?v=${KRIOS_ASSET_REVISION}`);
    expect(krios.driver?.hit).toContain(`?v=${KRIOS_ASSET_REVISION}`);
    expect(krios.driver?.victory).toContain(`?v=${KRIOS_ASSET_REVISION}`);
    expect(krios.stats).toEqual({
      speed: 10,
      acceleration: 4,
      weight: 9,
      handling: 3,
      miniTurbo: 4,
      traction: 6,
    });
  });

  it('maps Keeg to The Mycelial Majesty and the approved AA-04 profile', () => {
    const keeg = characterById('aa-04');
    expect(keeg.displayName).toBe('Keeg');
    expect(keeg.descriptor).toBe('Balanced Racer');
    expect(keeg.assetState).toBe('production');
    expect(keeg.kartName).toBe('The Mycelial Majesty');
    expect(keeg.kart).toContain(`/assets/characters/aa-04/kart.glb?v=${KEEG_ASSET_REVISION}`);
    expect(keeg.kartVisualYaw).toBe(NEGATIVE_Z_KART_VISUAL_YAW);
    expect(keeg.driverSpritePosition).toEqual([0, 0.72, -0.12]);
    expect(keeg.driver?.rear).toContain(`?v=${KEEG_ASSET_REVISION}`);
    expect(keeg.driver?.front).toContain(`?v=${KEEG_ASSET_REVISION}`);
    expect(keeg.driver?.steerLeft).toContain(`?v=${KEEG_ASSET_REVISION}`);
    expect(keeg.driver?.steerRight).toContain(`?v=${KEEG_ASSET_REVISION}`);
    expect(keeg.driver?.hit).toContain(`?v=${KEEG_ASSET_REVISION}`);
    expect(keeg.driver?.victory).toContain(`?v=${KEEG_ASSET_REVISION}`);
    expect(keeg.stats).toEqual({
      speed: 7,
      acceleration: 7,
      weight: 5,
      handling: 7,
      miniTurbo: 5,
      traction: 5,
    });
  });

  it('maps McFleurdel to The Fleur de Nuit and the approved AA-07 profile', () => {
    const mcfleurdel = characterById('aa-07');
    expect(mcfleurdel.displayName).toBe('McFleurdel');
    expect(mcfleurdel.descriptor).toBe('High-Speed Cruiser');
    expect(mcfleurdel.assetState).toBe('production');
    expect(mcfleurdel.kartName).toBe('The Fleur de Nuit');
    expect(mcfleurdel.kart).toContain(
      `/assets/characters/aa-07/kart.glb?v=${MCFLEURDEL_ASSET_REVISION}`,
    );
    expect(mcfleurdel.kartVisualYaw).toBe(NEGATIVE_Z_KART_VISUAL_YAW);
    expect(mcfleurdel.driver?.rear).toContain(`?v=${MCFLEURDEL_ASSET_REVISION}`);
    expect(mcfleurdel.driver?.front).toContain(`?v=${MCFLEURDEL_ASSET_REVISION}`);
    expect(mcfleurdel.driver?.steerLeft).toContain(`?v=${MCFLEURDEL_ASSET_REVISION}`);
    expect(mcfleurdel.driver?.steerRight).toContain(`?v=${MCFLEURDEL_ASSET_REVISION}`);
    expect(mcfleurdel.driver?.hit).toContain(`?v=${MCFLEURDEL_ASSET_REVISION}`);
    expect(mcfleurdel.driver?.victory).toContain(`?v=${MCFLEURDEL_ASSET_REVISION}`);
    expect(mcfleurdel.stats).toEqual({
      speed: 8,
      acceleration: 6,
      weight: 7,
      handling: 5,
      miniTurbo: 4,
      traction: 6,
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
    expect(lavi.frontDriverSpritePosition).toEqual([0, 0.45, -0.12]);
    expect(lavi.driver?.front).toContain(`?v=${LAVI_ASSET_REVISION}`);
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
  it('maps Toph to The Grave Shift and the approved AA-08 profile', () => {
    const toph = characterById('aa-08');
    expect(toph.displayName).toBe('Toph');
    expect(toph.descriptor).toBe('Turbo Bruiser');
    expect(toph.assetState).toBe('production');
    expect(toph.kartName).toBe('The Grave Shift');
    expect(toph.kart).toContain(`/assets/characters/aa-08/kart.glb?v=${TOPH_ASSET_REVISION}`);
    expect(toph.kartVisualYaw).toBe(NEGATIVE_Z_KART_VISUAL_YAW);
    expect(toph.frontDriverSpritePosition).toEqual([0, 0.45, -0.12]);
    expect(toph.driver?.rear).toContain(`?v=${TOPH_ASSET_REVISION}`);
    expect(toph.driver?.front).toContain(`?v=${TOPH_ASSET_REVISION}`);
    expect(toph.driver?.steerLeft).toContain(`?v=${TOPH_ASSET_REVISION}`);
    expect(toph.driver?.steerRight).toContain(`?v=${TOPH_ASSET_REVISION}`);
    expect(toph.driver?.hit).toContain(`?v=${TOPH_ASSET_REVISION}`);
    expect(toph.driver?.victory).toContain(`?v=${TOPH_ASSET_REVISION}`);
    expect(toph.stats).toEqual({
      speed: 7,
      acceleration: 5,
      weight: 7,
      handling: 4,
      miniTurbo: 8,
      traction: 5,
    });
  });

  it('maps Lula to The Verdant Hart and the approved AA-03 profile', () => {
    const lula = characterById('aa-03');
    expect(lula.displayName).toBe('Lula');
    expect(lula.descriptor).toBe('Feather Dirt Ace');
    expect(lula.assetState).toBe('production');
    expect(lula.kartName).toBe('The Verdant Hart');
    expect(lula.kart).toContain(`/assets/characters/aa-03/kart.glb?v=${LULA_ASSET_REVISION}`);
    expect(lula.kartVisualYaw).toBe(NEGATIVE_Z_KART_VISUAL_YAW);
    expect(lula.frontDriverSpritePosition).toEqual([0, 0.45, -0.12]);
    expect(lula.driver?.rear).toContain(`?v=${LULA_ASSET_REVISION}`);
    expect(lula.driver?.front).toContain(`?v=${LULA_ASSET_REVISION}`);
    expect(lula.driver?.steerLeft).toContain(`?v=${LULA_ASSET_REVISION}`);
    expect(lula.driver?.steerRight).toContain(`?v=${LULA_ASSET_REVISION}`);
    expect(lula.driver?.hit).toContain(`?v=${LULA_ASSET_REVISION}`);
    expect(lula.driver?.victory).toContain(`?v=${LULA_ASSET_REVISION}`);
    expect(lula.stats).toEqual({
      speed: 5,
      acceleration: 8,
      weight: 3,
      handling: 7,
      miniTurbo: 6,
      traction: 7,
    });
  });
});
