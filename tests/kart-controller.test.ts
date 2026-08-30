import RAPIER from '@dimforge/rapier3d-compat';
import { Vector3 } from 'three';
import { beforeAll, describe, expect, it } from 'vitest';
import { characterManifest } from '../src/characters/manifest';
import {
  createKartTuning,
  sliceOneDriver,
  surfaceSpeedMultiplier,
  type DriverStats,
} from '../src/config/kartTuning';
import { KartController, type DriveInput } from '../src/game/physics/KartController';

describe('Rapier kart controller', () => {
  beforeAll(async () => {
    await RAPIER.init();
  });

  function makeKart(stats: DriverStats = sliceOneDriver): {
    world: RAPIER.World;
    kart: KartController;
  } {
    const world = new RAPIER.World({ x: 0, y: -18, z: 0 });
    world.timestep = 1 / 60;
    world.createCollider(RAPIER.ColliderDesc.cuboid(500, 0.1, 500).setTranslation(0, -0.12, 0));
    return {
      world,
      kart: new KartController(world, createKartTuning(stats), stats, new Vector3(0, 1.1, 0), 0),
    };
  }

  function step(
    world: RAPIER.World,
    kart: KartController,
    input: DriveInput,
    count: number,
    surface: 'asphalt' | 'dirt' | 'grass' = 'asphalt',
  ): void {
    for (let index = 0; index < count; index += 1) {
      kart.update(input, surface, 1 / 60);
      world.step();
    }
  }

  it('charges purple, releases the highest tier, and stays finite', () => {
    const { world, kart } = makeKart();
    step(world, kart, { throttle: 1, steering: 0, brake: false, drift: false }, 180);
    step(world, kart, { throttle: 1, steering: 1, brake: false, drift: true }, 260);

    expect(kart.feedback().driftTier).toBe('purple');
    step(world, kart, { throttle: 1, steering: 1, brake: false, drift: false }, 1);
    expect(kart.feedback()).toMatchObject({ driftTier: 'purple', boostActive: true });
    expect(kart.isFinite()).toBe(true);
  });

  it('keeps sustained grass driving above the playable floor', () => {
    const { world, kart } = makeKart();
    step(world, kart, { throttle: 1, steering: 0, brake: false, drift: false }, 600, 'grass');
    expect(kart.speedMetersPerSecond()).toBeGreaterThanOrEqual(8.4);
  });

  it('makes every roster profile sustain its Speed-defined asphalt maximum', () => {
    for (const character of characterManifest) {
      const { world, kart } = makeKart(character.stats);
      step(world, kart, { throttle: 1, steering: 0, brake: false, drift: false }, 600);
      expect(kart.speedMetersPerSecond(), character.displayName).toBeCloseTo(
        createKartTuning(character.stats).maxSpeed,
        1,
      );
    }
  });

  it('uses Acceleration for time-to-speed without changing sustained top speed', () => {
    const lowAcceleration: DriverStats = {
      speed: 8,
      acceleration: 4,
      weight: 5,
      handling: 5,
      miniTurbo: 5,
      traction: 5,
    };
    const highAcceleration = { ...lowAcceleration, acceleration: 8 };
    const low = makeKart(lowAcceleration);
    const high = makeKart(highAcceleration);

    step(low.world, low.kart, { throttle: 1, steering: 0, brake: false, drift: false }, 60);
    step(high.world, high.kart, { throttle: 1, steering: 0, brake: false, drift: false }, 60);
    expect(high.kart.speedMetersPerSecond() - low.kart.speedMetersPerSecond()).toBeGreaterThan(2);

    step(low.world, low.kart, { throttle: 1, steering: 0, brake: false, drift: false }, 120);
    step(high.world, high.kart, { throttle: 1, steering: 0, brake: false, drift: false }, 120);
    expect(low.kart.speedMetersPerSecond()).toBeLessThan(
      createKartTuning(lowAcceleration).maxSpeed * 0.75,
    );

    step(low.world, low.kart, { throttle: 1, steering: 0, brake: false, drift: false }, 420);
    step(high.world, high.kart, { throttle: 1, steering: 0, brake: false, drift: false }, 420);
    const expectedMaximum = createKartTuning(lowAcceleration).maxSpeed;
    expect(low.kart.speedMetersPerSecond()).toBeCloseTo(expectedMaximum, 1);
    expect(high.kart.speedMetersPerSecond()).toBeCloseTo(expectedMaximum, 1);
  });

  it('slows progressively when entering dirt or grass', () => {
    for (const surface of ['dirt', 'grass'] as const) {
      const { world, kart } = makeKart();
      step(world, kart, { throttle: 1, steering: 0, brake: false, drift: false }, 600);
      const asphaltSpeed = kart.speedMetersPerSecond();

      step(world, kart, { throttle: 1, steering: 0, brake: false, drift: false }, 1, surface);
      expect(kart.speedMetersPerSecond()).toBeGreaterThan(asphaltSpeed - 0.3);

      step(world, kart, { throttle: 1, steering: 0, brake: false, drift: false }, 240, surface);
      const expectedSurfaceMaximum =
        createKartTuning(sliceOneDriver).maxSpeed *
        surfaceSpeedMultiplier(surface, sliceOneDriver.traction);
      expect(kart.speedMetersPerSecond()).toBeCloseTo(expectedSurfaceMaximum, 1);
    }
  });
});
