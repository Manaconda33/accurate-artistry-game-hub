import { describe, expect, it } from 'vitest';
import {
  isDriverFrontFacingCamera,
  selectDriverFrame,
  shouldShowModeledSteeringControl,
} from '../src/game/driver/DriverSpriteState';

describe('shared driver sprite state', () => {
  it('uses the front frame when the camera is ahead of that racer', () => {
    expect(
      selectDriverFrame({
        finished: false,
        frontFacingCamera: true,
        hitSeconds: 0,
        steering: 0,
      }),
    ).toBe('front');
  });

  it('determines facing independently for same-direction and oncoming racers', () => {
    const camera = { x: 0, z: 4 };
    expect(
      isDriverFrontFacingCamera({ x: 0, z: 0 }, { x: 0, z: 1 }, camera),
    ).toBe(true);
    expect(
      isDriverFrontFacingCamera({ x: 0, z: 8 }, { x: 0, z: 1 }, camera),
    ).toBe(false);
    expect(
      isDriverFrontFacingCamera({ x: 0, z: 8 }, { x: 0, z: -1 }, camera),
    ).toBe(true);
  });

  it('maps positive and negative steering to the matching turn frames', () => {
    expect(
      selectDriverFrame({
        finished: false,
        frontFacingCamera: false,
        hitSeconds: 0,
        steering: 0.3,
      }),
    ).toBe('steerLeft');
    expect(
      selectDriverFrame({
        finished: false,
        frontFacingCamera: false,
        hitSeconds: 0,
        steering: -0.3,
      }),
    ).toBe('steerRight');
  });

  it('gives finish and collision reactions priority over camera and steering', () => {
    expect(
      selectDriverFrame({
        finished: false,
        frontFacingCamera: true,
        hitSeconds: 0.2,
        steering: 1,
      }),
    ).toBe('hit');
    expect(
      selectDriverFrame({
        finished: true,
        frontFacingCamera: true,
        hitSeconds: 0.2,
        steering: 1,
      }),
    ).toBe('victory');
  });

  it('returns to the neutral rear frame inside the steering dead zone', () => {
    expect(
      selectDriverFrame({
        finished: false,
        frontFacingCamera: false,
        hitSeconds: 0,
        steering: 0.15,
      }),
    ).toBe('rear');
  });

  it('uses Accu\'s baked control for rear states and the modeled control for front view', () => {
    for (const frame of ['rear', 'steerLeft', 'steerRight', 'hit', 'victory'] as const) {
      expect(shouldShowModeledSteeringControl(true, frame)).toBe(false);
    }
    expect(shouldShowModeledSteeringControl(true, 'front')).toBe(true);
    expect(shouldShowModeledSteeringControl(false, 'rear')).toBe(true);
  });
});
