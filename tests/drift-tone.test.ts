import { describe, expect, it, vi } from 'vitest';
import { playDriftTierTone, resumeAudioContext } from '../src/audio/driftTone';

describe('drift tier audio', () => {
  it('does not throw when the browser audio context is unavailable', async () => {
    expect(playDriftTierTone('blue', undefined)).toBe(false);
    await expect(resumeAudioContext(null)).resolves.toBe(false);
  });

  it('contains Web Audio failures so gameplay can continue', () => {
    const context = {
      state: 'running',
      createOscillator: () => {
        throw new Error('Web Audio unavailable');
      },
    } as unknown as AudioContext;

    expect(() => playDriftTierTone('orange', context)).not.toThrow();
    expect(playDriftTierTone('orange', context)).toBe(false);
  });

  it('contains rejected audio resume attempts', async () => {
    const context = {
      state: 'suspended',
      resume: vi.fn().mockRejectedValue(new Error('Audio blocked')),
    } as unknown as AudioContext;

    await expect(resumeAudioContext(context)).resolves.toBe(false);
  });
});
