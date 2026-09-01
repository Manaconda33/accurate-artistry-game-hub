import { describe, expect, it } from 'vitest';
import {
  driverFrameFallbacks,
  isDriverFrontFacingCamera,
  isFrontFacingDriverFrame,
  modeledSteeringControlPosition,
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
    expect(isDriverFrontFacingCamera({ x: 0, z: 0 }, { x: 0, z: 1 }, camera)).toBe(true);
    expect(isDriverFrontFacingCamera({ x: 0, z: 8 }, { x: 0, z: 1 }, camera)).toBe(false);
    expect(isDriverFrontFacingCamera({ x: 0, z: 8 }, { x: 0, z: -1 }, camera)).toBe(true);
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

    expect(
      selectDriverFrame({
        finished: false,
        frontFacingCamera: true,
        hitSeconds: 0,
        steering: 0.3,
      }),
    ).toBe('frontSteerLeft');
    expect(
      selectDriverFrame({
        finished: false,
        frontFacingCamera: true,
        hitSeconds: 0,
        steering: -0.3,
      }),
    ).toBe('frontSteerRight');
  });

  it('gives finish and collision reactions priority over camera and steering', () => {
    expect(
      selectDriverFrame({
        finished: false,
        frontFacingCamera: true,
        hitSeconds: 0.2,
        steering: 1,
      }),
    ).toBe('frontHit');
    expect(
      selectDriverFrame({
        finished: true,
        frontFacingCamera: true,
        hitSeconds: 0.2,
        steering: 1,
      }),
    ).toBe('frontVictory');
  });

  it('falls missing front actions back to neutral front before rear', () => {
    expect(driverFrameFallbacks('frontSteerLeft')).toEqual(['frontSteerLeft', 'front', 'rear']);
    expect(driverFrameFallbacks('frontHit')).toEqual(['frontHit', 'front', 'rear']);
    expect(driverFrameFallbacks('frontVictory')).toEqual(['frontVictory', 'front', 'rear']);
    expect(driverFrameFallbacks('hit')).toEqual(['hit', 'rear']);
  });

  it('classifies every camera-facing action as front-facing', () => {
    for (const frame of [
      'front',
      'frontSteerLeft',
      'frontSteerRight',
      'frontHit',
      'frontVictory',
    ] as const) {
      expect(isFrontFacingDriverFrame(frame)).toBe(true);
    }
    expect(isFrontFacingDriverFrame('rear')).toBe(false);
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

  it("uses Accu's baked control for rear states and the modeled control for front view", () => {
    for (const frame of ['rear', 'steerLeft', 'steerRight', 'hit', 'victory'] as const) {
      expect(shouldShowModeledSteeringControl(true, frame)).toBe(false);
    }
    for (const frame of [
      'front',
      'frontSteerLeft',
      'frontSteerRight',
      'frontHit',
      'frontVictory',
    ] as const) {
      expect(shouldShowModeledSteeringControl(true, frame)).toBe(true);
    }
    expect(shouldShowModeledSteeringControl(false, 'rear')).toBe(true);
  });

  it('moves a modeled control only for its front-facing frame and restores its authored position', () => {
    const authored = [0, 1.46, 0.48] as const;
    const front = [0, 1.46, -0.46] as const;

    for (const frame of [
      'front',
      'frontSteerLeft',
      'frontSteerRight',
      'frontHit',
      'frontVictory',
    ] as const) {
      expect(modeledSteeringControlPosition(frame, authored, front)).toBe(front);
    }
    for (const frame of ['rear', 'steerLeft', 'steerRight', 'hit', 'victory'] as const) {
      expect(modeledSteeringControlPosition(frame, authored, front)).toBe(authored);
    }
  });
});
