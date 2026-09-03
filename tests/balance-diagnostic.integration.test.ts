import RAPIER from '@dimforge/rapier3d-compat';
import { beforeAll, describe, expect, it } from 'vitest';
import { characterManifest } from '../src/characters/manifest';
import { createKartTuning } from '../src/config/kartTuning';
import { AiDriver, type AiDriverProfile } from '../src/game/ai/AiDriver';
import { KartController } from '../src/game/physics/KartController';
import { LapTracker } from '../src/game/race/LapTracker';
import { CircuitAlpha } from '../src/game/track/CircuitAlpha';

interface DiagnosticResult {
  racer: string;
  profile: string;
  finishSeconds: number;
  grassRatio: number;
  maxLateralDistance: number;
  maxSpeed: number;
}

describe('candidate balance physics diagnostic', () => {
  beforeAll(async () => {
    await RAPIER.init();
  });

  const profiles: readonly { name: string; value: AiDriverProfile }[] = [
    {
      name: 'conservative-left',
      value: { laneOffset: -1.05, pace: 0.28, aggression: 0.2 },
    },
    {
      name: 'aggressive-dirt',
      value: { laneOffset: 1.4, pace: 0.55, aggression: 0.8 },
    },
    {
      name: 'fast-left',
      value: { laneOffset: -2.1, pace: 0.82, aggression: 0.6 },
    },
  ];

  function runRace(
    racer: (typeof characterManifest)[number],
    profile: AiDriverProfile,
  ): Omit<DiagnosticResult, 'racer' | 'profile'> {
    const track = new CircuitAlpha();
    const world = new RAPIER.World({ x: 0, y: -18, z: 0 });
    world.timestep = 1 / 60;
    world.createCollider(RAPIER.ColliderDesc.cuboid(450, 0.1, 450).setTranslation(0, -0.12, 0));

    const tangent = track.checkpointTangent(0);
    const tuning = createKartTuning(racer.stats);
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
    let grassFrames = 0;
    let simulatedFrames = 0;
    let maximumLateralDistance = 0;
    let observedMaximumSpeed = 0;
    let finishSeconds: number | null = null;

    for (let step = 0; step < 14_400 && !laps.snapshot().finished; step += 1) {
      const position = kart.position();
      const projection = track.project(position);
      simulatedFrames += 1;
      if (projection.surface === 'grass') grassFrames += 1;
      maximumLateralDistance = Math.max(maximumLateralDistance, projection.lateralDistance);
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

    const snapshot = laps.snapshot();
    expect(snapshot.finished, racer.displayName).toBe(true);
    expect(kart.isFinite(), racer.displayName).toBe(true);
    expect(grassFrames / simulatedFrames, racer.displayName).toBeLessThan(0.02);
    expect(maximumLateralDistance, racer.displayName).toBeLessThan(track.roadHalfWidth + 0.5);

    return {
      finishSeconds: finishSeconds ?? simulatedFrames / 60,
      grassRatio: grassFrames / simulatedFrames,
      maxLateralDistance: maximumLateralDistance,
      maxSpeed: observedMaximumSpeed,
    };
  }

  it(
    'records representative three-lap physics baselines for every manifest racer',
    () => {
      const results: DiagnosticResult[] = [];
      for (const racer of characterManifest) {
        for (const profile of profiles) {
          results.push({
            racer: racer.displayName,
            profile: profile.name,
            ...runRace(racer, profile.value),
          });
        }
      }

      console.log(`BALANCE_DIAGNOSTIC ${JSON.stringify(results)}`);
      expect(results).toHaveLength(characterManifest.length * profiles.length);
    },
    90_000,
  );
});
