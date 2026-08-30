import { describe, expect, it } from 'vitest';
import { collisionImpulseShares, collisionSpeedRetention } from '../src/game/physics/KartCollision';

describe('relative-mass kart collision response', () => {
  it('displaces a lighter kart more than a heavier kart', () => {
    const shares = collisionImpulseShares(110, 175, 55);
    expect(shares.first).toBeGreaterThan(shares.second);
    expect(shares.first + shares.second).toBeCloseTo(55);
  });

  it('does not penalize overlapping karts without a meaningful impact', () => {
    expect(collisionSpeedRetention(5, 5, 0.74)).toBe(1);
  });

  it('gives heavy racers a measurable but bounded speed-retention advantage', () => {
    const heavyRetention = collisionSpeedRetention(10, 2, 16);
    const lightRetention = collisionSpeedRetention(2, 10, 16);

    expect(heavyRetention).toBeCloseTo(0.8592, 4);
    expect(lightRetention).toBeCloseTo(0.6715, 4);
    expect(heavyRetention - lightRetention).toBeGreaterThan(0.15);
    expect(heavyRetention).toBeLessThanOrEqual(0.87);
  });

  it('keeps collision retention inside the governed risk range', () => {
    for (let weight = 1; weight <= 10; weight += 1) {
      for (let otherWeight = 1; otherWeight <= 10; otherWeight += 1) {
        const retention = collisionSpeedRetention(weight, otherWeight, 16);
        expect(retention).toBeGreaterThanOrEqual(0.65);
        expect(retention).toBeLessThanOrEqual(0.96);
      }
    }
  });
});
