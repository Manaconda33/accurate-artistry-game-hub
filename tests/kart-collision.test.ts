import { describe, expect, it } from 'vitest';
import { collisionImpulseShares } from '../src/game/physics/KartCollision';

describe('relative-mass kart collision response', () => {
  it('displaces a lighter kart more than a heavier kart', () => {
    const shares = collisionImpulseShares(110, 175, 55);
    expect(shares.first).toBeGreaterThan(shares.second);
    expect(shares.first + shares.second).toBeCloseTo(55);
  });
});
