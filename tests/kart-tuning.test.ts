import { describe, expect, it } from 'vitest';
import {
  aiCornerTargetSpeed,
  aiDriftTargetTier,
  aiRequestedDriftTier,
  createKartTuning,
  driftBoostProfile,
  driftThresholds,
  handlingCornerSpeedMultiplier,
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

  it('compresses the Speed 1-10 spread while preserving strict ordering', () => {
    const slowest = createKartTuning({ ...sliceOneDriver, speed: 1 }).maxSpeed;
    const middle = createKartTuning({ ...sliceOneDriver, speed: 5 }).maxSpeed;
    const acceptedCenter = createKartTuning({ ...sliceOneDriver, speed: 7 }).maxSpeed;
    const fastest = createKartTuning({ ...sliceOneDriver, speed: 10 }).maxSpeed;

    expect(slowest).toBeCloseTo(27.5);
    expect(middle).toBeCloseTo(28.8333, 3);
    expect(acceptedCenter).toBeCloseTo(29.5);
    expect(fastest).toBeCloseTo(30.5);
    expect(fastest - slowest).toBeCloseTo(3);
    expect(slowest).toBeLessThan(middle);
    expect(middle).toBeLessThan(acceptedCenter);
    expect(acceptedCenter).toBeLessThan(fastest);
  });

  it('uses the PRD launch-acceleration curve', () => {
    expect(createKartTuning({ ...sliceOneDriver, acceleration: 4 }).acceleration).toBeCloseTo(6.2);
    expect(createKartTuning({ ...sliceOneDriver, acceleration: 8 }).acceleration).toBeCloseTo(8.4);
  });

  it('lets Handling preserve more speed under equivalent steering demand', () => {
    expect(handlingCornerSpeedMultiplier(2, 0)).toBe(1);
    expect(handlingCornerSpeedMultiplier(9, 0)).toBe(1);
    expect(handlingCornerSpeedMultiplier(2, 1)).toBeCloseTo(0.8144, 3);
    expect(handlingCornerSpeedMultiplier(9, 1)).toBeCloseTo(0.9156, 3);
    expect(handlingCornerSpeedMultiplier(9, 1)).toBeGreaterThan(
      handlingCornerSpeedMultiplier(2, 1),
    );
    expect(handlingCornerSpeedMultiplier(9, 1)).toBeLessThan(1);
  });

  it('keeps AI anticipation modest so shared Handling physics remains the primary corner limit', () => {
    const lowHandling = aiCornerTargetSpeed(30, 0.6, 0.5, 1, 2);
    const highHandling = aiCornerTargetSpeed(30, 0.6, 0.5, 1, 9);
    expect(highHandling).toBeGreaterThan(lowHandling);
    expect(highHandling - lowHandling).toBeLessThan(0.2);
    expect(lowHandling).toBeGreaterThan(29);
    expect(aiCornerTargetSpeed(30, 0.6, 0, 1, 2)).toBe(30);
    expect(aiCornerTargetSpeed(30, 0.6, 0, 1.04, 9)).toBeCloseTo(31.2);

    const conservativeFullCorner = aiCornerTargetSpeed(30, 0.28, 1, 1, 5);
    const fastFullCorner = aiCornerTargetSpeed(30, 0.82, 1, 1, 5);
    expect(conservativeFullCorner).toBeGreaterThan(27.3);
    expect(fastFullCorner).toBeGreaterThan(conservativeFullCorner);
    expect(fastFullCorner).toBeGreaterThan(28.4);
  });

  it('makes high Mini-Turbo seek drift opportunities at lower turn demand', () => {
    expect(aiRequestedDriftTier(0.2, 0.6, 12, 0.3, 2)).toBeUndefined();
    expect(aiRequestedDriftTier(0.2, 0.6, 12, 0.3, 9)).toBe('blue');
    expect(aiRequestedDriftTier(0.3, 0.79, 18, 0.5, 9)).toBe('purple');
    expect(aiRequestedDriftTier(0.3, 0.79, 18, 0.5, 4)).toBe('orange');
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

  it('limits AI drift reward tier according to the Mini-Turbo stat', () => {
    expect(aiDriftTargetTier('purple', 4)).toBe('blue');
    expect(aiDriftTargetTier('purple', 6)).toBe('orange');
    expect(aiDriftTargetTier('purple', 9)).toBe('purple');
    expect(aiDriftTargetTier('orange', 7)).toBe('orange');
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
