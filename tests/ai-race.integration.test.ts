import RAPIER from '@dimforge/rapier3d-compat';
import { beforeAll, describe, expect, it } from 'vitest';
import { createKartTuning, sliceOneDriver } from '../src/config/kartTuning';
import { AiDriver } from '../src/game/ai/AiDriver';
import { KartController } from '../src/game/physics/KartController';
import { LapTracker } from '../src/game/race/LapTracker';
import { CircuitAlpha } from '../src/game/track/CircuitAlpha';

describe('Rapier spline AI integration', () => {
  beforeAll(async () => {
    await RAPIER.init();
  });

  it('qualifies all seven AI profiles over three validated laps without player input', () => {
    const track = new CircuitAlpha();
    const profiles = Array.from({ length: 7 }, (_, index) => ({
      laneOffset: (index % 2 === 0 ? -1 : 1) * (0.35 + Math.floor(index / 2) * 0.25),
      pace: 0.28 + index * 0.09,
      aggression: 0.2 + (index % 4) * 0.2,
    }));

    for (const profile of profiles) {
      const world = new RAPIER.World({ x: 0, y: -18, z: 0 });
      world.timestep = 1 / 60;
      world.createCollider(RAPIER.ColliderDesc.cuboid(450, 0.1, 450).setTranslation(0, -0.12, 0));
      const tangent = track.checkpointTangent(0);
      const kart = new KartController(
        world,
        createKartTuning(sliceOneDriver),
        sliceOneDriver,
        track.checkpointPosition(0).addScaledVector(tangent, 8),
        Math.atan2(tangent.x, tangent.z),
      );
      const driver = new AiDriver(track, profile);
      const laps = new LapTracker();
      let overlap = -1;

      for (let step = 0; step < 21_600 && !laps.snapshot().finished; step += 1) {
        const position = kart.position();
        const projection = track.project(position);
        kart.update(
          driver.input(position, kart.forward(), kart.speedMetersPerSecond()),
          projection.surface,
          1 / 60,
        );
        world.step();
        let checkpoint = -1;
        for (let index = 0; index < track.checkpointIndices.length; index += 1) {
          if (position.distanceToSquared(track.checkpointPosition(index)) < 13 * 13) {
            checkpoint = index;
            break;
          }
        }
        if (checkpoint !== -1 && checkpoint !== overlap) {
          laps.enterCheckpoint(checkpoint, kart.forward().dot(projection.tangent), step / 60);
        }
        overlap = checkpoint;
      }

      expect(laps.snapshot().finished).toBe(true);
      expect(kart.isFinite()).toBe(true);
    }
  }, 30_000);
});
