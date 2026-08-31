import { describe, expect, it } from 'vitest';
import { selectDriverFrame } from '../src/game/driver/DriverSpriteState';

describe('shared driver sprite state', () => {
  it('uses the front frame for every racer while the rear-view camera is active', () => {
    expect(selectDriverFrame({ finished: false, hitSeconds: 0, rearView: true, steering: 0 })).toBe(
      'front',
    );
  });

  it('maps positive and negative steering to the matching turn frames', () => {
    expect(
      selectDriverFrame({ finished: false, hitSeconds: 0, rearView: false, steering: 0.3 }),
    ).toBe('steerLeft');
    expect(
      selectDriverFrame({ finished: false, hitSeconds: 0, rearView: false, steering: -0.3 }),
    ).toBe('steerRight');
  });

  it('gives finish and collision reactions priority over camera and steering', () => {
    expect(
      selectDriverFrame({ finished: false, hitSeconds: 0.2, rearView: true, steering: 1 }),
    ).toBe('hit');
    expect(
      selectDriverFrame({ finished: true, hitSeconds: 0.2, rearView: true, steering: 1 }),
    ).toBe('victory');
  });

  it('returns to the neutral rear frame inside the steering dead zone', () => {
    expect(
      selectDriverFrame({ finished: false, hitSeconds: 0, rearView: false, steering: 0.15 }),
    ).toBe('rear');
  });
});
