import { describe, expect, it } from 'vitest';
import {
  createKartTuning,
  driftBoostProfile,
  driftThresholds,
  sliceOneDriver,
  surfaceAccelerationMultiplier,
  surfaceMinimumPlayableSpeed,
  surfaceSpeedMultiplier,
} from '../src/config/kartTuning';

describe('kart tuning and surface behavior', () => {
  it('maps character stats into finite physics values', () => {
    const tuning = createKartTuning(sliceOneDriver);
    for (const value of Object.values(tuning)) expect(Number.isFinite(value)).toBe(true);
    expect(tuning.maxSpeed).toBeGreaterThan(23);
    expect(tuning.mass).toBeGreaterThan(105);
  });

  it('uses the PRD launch-acceleration curve', () => {
    expect(createKartTuning({ ...sliceOneDriver, acceleration: 4 }).acceleration).toBeCloseTo(6.2);
    expect(createKartTuning({ ...sliceOneDriver, acceleration: 8 }).acceleration).toBeCloseTo(8.4);
  });

  it('makes grass slower than dirt and asphalt', () => {
    const traction = sliceOneDriver.traction;
    expect(surfaceSpeedMultiplier('grass', traction)).toBeLessThan(
      surfaceSpeedMultiplier('dirt', traction),
    );
    expect(surfaceSpeedMultiplier('dirt', traction)).toBeLessThan(1);
    expect(surfaceAccelerationMultiplier('grass', traction)).toBeLessThan(
      surfaceAccelerationMultiplier('dirt', traction),
    );
    expect(surfaceMinimumPlayableSpeed('grass')).toBeGreaterThan(0);
    expect(surfaceMinimumPlayableSpeed('dirt')).toBeGreaterThan(
      surfaceMinimumPlayableSpeed('grass'),
    );
  });

  it('orders all three drift tiers and rewards higher Mini-Turbo', () => {
    const low = driftThresholds(1);
    const high = driftThresholds(10);
    expect(low.blue).toBeLessThan(low.orange);
    expect(low.orange).toBeLessThan(low.purple);
    expect(high.blue).toBeLessThan(low.blue);
    expect(high.purple).toBeLessThan(low.purple);

    const blue = driftBoostProfile('blue', 5);
    const orange = driftBoostProfile('orange', 5);
    const purple = driftBoostProfile('purple', 5);
    expect(blue.duration).toBeLessThan(orange.duration);
    expect(orange.duration).toBeLessThan(purple.duration);
    expect(blue.speedMultiplier).toBeLessThan(purple.speedMultiplier);
  });

  it('keeps a ten-minute fixed-step numeric soak finite', () => {
    const tuning = createKartTuning(sliceOneDriver);
    const dt = 1 / 60;
    let speed = 0;
    let yaw = 0;
    let x = 0;
    let z = 0;

    for (let step = 0; step < 10 * 60 * 60; step += 1) {
      const steering = Math.sin(step / 240) * tuning.steeringRate;
      speed = Math.min(tuning.maxSpeed, speed + tuning.acceleration * dt);
      yaw += steering * dt;
      x += Math.sin(yaw) * speed * dt;
      z += Math.cos(yaw) * speed * dt;
      expect([speed, yaw, x, z].every(Number.isFinite)).toBe(true);
    }
  });
});
