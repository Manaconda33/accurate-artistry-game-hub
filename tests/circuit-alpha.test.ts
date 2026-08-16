import { describe, expect, it } from 'vitest';
import { CircuitAlpha } from '../src/game/track/CircuitAlpha';

describe('Circuit Alpha topology', () => {
  const track = new CircuitAlpha();

  it('provides a shortened manual-test loop and twelve checkpoints', () => {
    expect(track.curve.getLength()).toBeGreaterThan(850);
    expect(track.curve.getLength()).toBeLessThan(950);
    expect(track.checkpointIndices).toHaveLength(12);
    expect(new Set(track.checkpointIndices).size).toBe(12);
  });

  it('projects the required Slice 1 surfaces from shared topology', () => {
    expect(track.project(track.curve.getPointAt(0.1)).surface).toBe('asphalt');
    const dirtPoint = track.curve.getPointAt(0.27);
    const dirtTangent = track.curve.getTangentAt(0.27);
    dirtPoint.x += dirtTangent.z * 3.8;
    dirtPoint.z -= dirtTangent.x * 3.8;
    expect(track.project(dirtPoint).surface).toBe('dirt');
    expect(track.project(track.curve.getPointAt(0.27)).surface).toBe('asphalt');
    expect(track.project(track.curve.getPointAt(0.45)).surface).toBe('boost');
    expect(track.project(track.curve.getPointAt(0.5)).surface).toBe('ramp');

    const grassPoint = track.curve.getPointAt(0.1);
    grassPoint.x += 40;
    expect(track.project(grassPoint).surface).toBe('grass');
  });
});
