import RAPIER from '@dimforge/rapier3d-compat';
import { beforeAll, describe, expect, it } from 'vitest';
import { characterManifest } from '../src/characters/manifest';
import { createKartTuning } from '../src/config/kartTuning';
import { AiDriver, type AiDriverProfile } from '../src/game/ai/AiDriver';
import { KartController } from '../src/game/physics/KartController';
import { LapTracker } from '../src/game/race/LapTracker';
import { CircuitAlpha } from '../src/game/track/CircuitAlpha';

interface CurveDefinition {
  name: string;
  minimum: number;
  spread: number;
}

interface SweepResult {
  curve: string;
  racer: string;
  profile: string;
  finishSeconds: number;
  maxSpeed: number;
}

describe('candidate Speed-curve sweep', () => {
  beforeAll(async () => {
    await RAPIER.init();
  });

  const curves: readonly CurveDefinition[] = [
    { name: 'B-3.00', minimum: 27.5, spread: 3 },
    { name: 'C-3.75', minimum: 27.25, spread: 3.75 },
    { name: 'D-4.50', minimum: 27, spread: 4.5 },
  ];
  const profiles: readonly { name: string; value: AiDriverProfile }[] = [
    { name: 'runtime-1', value: { laneOffset: -1.05, pace: 0.28, aggression: 0.2 } },
    { name: 'runtime-7', value: { laneOffset: -2.1, pace: 0.82, aggression: 0.6 } },
  ];

  function candidateMaximum(speed: number, curve: CurveDefinition): number {
    return curve.minimum + ((speed - 1) / 9) * curve.spread;
  }

  function runRace(
    racer: (typeof characterManifest)[number],
    profile: AiDriverProfile,
    curve: CurveDefinition,
  ): { finishSeconds: number; maxSpeed: number } {
    const track = new CircuitAlpha();
    const world = new RAPIER.World({ x: 0, y: -18, z: 0 });
    world.timestep = 1 / 60;
    world.createCollider(RAPIER.ColliderDesc.cuboid(450, 0.1, 450).setTranslation(0, -0.12, 0));

    const tangent = track.checkpointTangent(0);
    const tuning = {
      ...createKartTuning(racer.stats),
      maxSpeed: candidateMaximum(racer.stats.speed, curve),
    };
    const kart = new KartController(
      world,
      tuning,
      racer.stats,
      track.checkpointPosition(0).addScaledVector(tangent, 8),
      Math.atan2(tangent.x, tangent.z),
    );
    const driver = new AiDriver(track, profile, tuning.maxSpeed);
    const laps = new LapTracker();
    let overlap = -1;
    let observedMaximumSpeed = 0;
    let finishSeconds: number | null = null;

    for (let step = 0; step < 14_400 && !laps.snapshot().finished; step += 1) {
      const position = kart.position();
      const projection = track.project(position);
      observedMaximumSpeed = Math.max(observedMaximumSpeed, kart.speedMetersPerSecond());
      kart.update(
        driver.input(position, kart.forward(), kart.speedMetersPerSecond()),
        projection.surface,
        1 / 60,
      );
      world.step();

      const nextPosition = kart.position();
      const nextProjection = track.project(nextPosition);
      let checkpoint = -1;
      for (let index = 0; index < track.checkpointIndices.length; index += 1) {
        if (nextPosition.distanceToSquared(track.lapCheckpointPosition(index)) < 13 * 13) {
          checkpoint = index;
          break;
        }
      }
      if (checkpoint !== -1 && checkpoint !== overlap) {
        laps.enterCheckpoint(
          checkpoint,
          kart.forward().dot(nextProjection.tangent),
          (step + 1) / 60,
        );
        if (laps.snapshot().finished) finishSeconds = (step + 1) / 60;
      }
      overlap = checkpoint;
    }

    expect(laps.snapshot().finished, `${curve.name} ${racer.displayName}`).toBe(true);
    expect(kart.isFinite(), `${curve.name} ${racer.displayName}`).toBe(true);
    return {
      finishSeconds: finishSeconds ?? 240,
      maxSpeed: observedMaximumSpeed,
    };
  }

  it(
    'measures tighter global Speed curves with the same Handling and Mini-Turbo behavior',
    () => {
      const results: SweepResult[] = [];
      for (const curve of curves) {
        for (const racer of characterManifest) {
          for (const profile of profiles) {
            results.push({
              curve: curve.name,
              racer: racer.displayName,
              profile: profile.name,
              ...runRace(racer, profile.value, curve),
            });
          }
        }
      }
      console.log(`BALANCE_SPEED_SWEEP ${JSON.stringify(results)}`);
      expect(results).toHaveLength(curves.length * characterManifest.length * profiles.length);
    },
    120_000,
  );
});
