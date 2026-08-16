import type { DriftTier } from '../game/physics/KartController';

export async function resumeAudioContext(
  context: AudioContext | null | undefined,
): Promise<boolean> {
  if (context === undefined || context === null) return false;
  if (context.state === 'running') return true;
  if (context.state !== 'suspended') return false;

  try {
    await context.resume();
    return (context.state as AudioContextState) === 'running';
  } catch {
    return false;
  }
}

export function playDriftTierTone(
  tier: Exclude<DriftTier, 'none'>,
  context: AudioContext | null | undefined,
): boolean {
  if (context?.state !== 'running') return false;

  try {
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    const frequency = tier === 'purple' ? 880 : tier === 'orange' ? 660 : 480;

    oscillator.frequency.setValueAtTime(frequency, context.currentTime);
    oscillator.type = 'sine';
    gain.gain.setValueAtTime(0.0001, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.09, context.currentTime + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + 0.16);
    oscillator.connect(gain).connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + 0.18);
    return true;
  } catch {
    return false;
  }
}
