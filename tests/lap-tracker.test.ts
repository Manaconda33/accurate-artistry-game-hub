import { describe, expect, it } from 'vitest';
import { LapTracker } from '../src/game/race/LapTracker';

describe('LapTracker', () => {
  it('requires every ordered checkpoint before incrementing a lap', () => {
    const tracker = new LapTracker(4, 3);
    tracker.reset(0);

    expect(tracker.enterCheckpoint(2, 1, 1)).toBe(false);
    expect(tracker.enterCheckpoint(0, 1, 2)).toBe(false);
    expect(tracker.snapshot().lap).toBe(0);

    expect(tracker.enterCheckpoint(1, 1, 3)).toBe(true);
    expect(tracker.enterCheckpoint(2, 1, 4)).toBe(true);
    expect(tracker.enterCheckpoint(3, 1, 5)).toBe(true);
    expect(tracker.enterCheckpoint(0, 1, 6)).toBe(true);
    expect(tracker.snapshot().lap).toBe(1);
  });

  it('rejects reverse finish-line crossings', () => {
    const tracker = new LapTracker(3, 3);
    tracker.reset(0);
    tracker.enterCheckpoint(1, 1, 1);
    tracker.enterCheckpoint(2, 1, 2);

    expect(tracker.enterCheckpoint(0, -1, 3)).toBe(false);
    expect(tracker.snapshot()).toMatchObject({ lap: 0, nextCheckpoint: 0 });
    expect(tracker.enterCheckpoint(0, 1, 4)).toBe(true);
    expect(tracker.snapshot().lap).toBe(1);
  });

  it('finishes after three consecutive valid laps', () => {
    const tracker = new LapTracker(3, 3);
    tracker.reset(0);
    for (let lap = 0; lap < 3; lap += 1) {
      tracker.enterCheckpoint(1, 1, lap * 3 + 1);
      tracker.enterCheckpoint(2, 1, lap * 3 + 2);
      tracker.enterCheckpoint(0, 1, lap * 3 + 3);
    }
    expect(tracker.snapshot()).toMatchObject({ lap: 3, finished: true });
  });
});
