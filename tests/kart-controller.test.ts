import RAPIER from '@dimforge/rapier3d-compat';
import { Vector3 } from 'three';
import { beforeAll, describe, expect, it } from 'vitest';
import { createKartTuning, sliceOneDriver } from '../src/config/kartTuning';
import { KartController, type DriveInput } from '../src/game/physics/KartController';

describe('Rapier kart controller', () => {
  beforeAll(async () => {
    await RAPIER.init();
  });

  function makeKart(): { world: RAPIER.World; kart: KartController } {
    const world = new RAPIER.World({ x: 0, y: -18, z: 0 });
    world.timestep = 1 / 60;
    world.createCollider(RAPIER.ColliderDesc.cuboid(500, 0.1, 500).setTranslation(0, -0.12, 0));
    return {
      world,
      kart: new KartController(
        world,
        createKartTuning(sliceOneDriver),
        sliceOneDriver,
        new Vector3(0, 1.1, 0),
        0,
      ),
    };
  }

  function step(
    world: RAPIER.World,
    kart: KartController,
    input: DriveInput,
    count: number,
    surface: 'asphalt' | 'grass' = 'asphalt',
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
});
