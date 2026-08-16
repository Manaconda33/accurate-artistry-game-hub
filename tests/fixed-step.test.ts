import { describe, expect, it } from 'vitest';
import { FixedStepRunner } from '../src/game/physics/FixedStepRunner';

describe('FixedStepRunner', () => {
  it('advances simulation in fixed 60 Hz steps', () => {
    const runner = new FixedStepRunner(1 / 60);
    const steps: number[] = [];

    runner.advance(1 / 30, (dt) => steps.push(dt));

    expect(steps).toEqual([1 / 60, 1 / 60]);
  });

  it('clamps long frames to avoid a spiral of death', () => {
    const runner = new FixedStepRunner(1 / 60, 0.1);
    let count = 0;
    runner.advance(4, () => {
      count += 1;
    });
    expect(count).toBeLessThanOrEqual(6);
  });
});
