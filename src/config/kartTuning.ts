export type SurfaceType = 'asphalt' | 'dirt' | 'grass' | 'boost' | 'ramp';

export interface DriverStats {
  speed: number;
  acceleration: number;
  weight: number;
  handling: number;
  miniTurbo: number;
  traction: number;
}

export interface KartTuning {
  maxSpeed: number;
  acceleration: number;
  mass: number;
  steeringRate: number;
  lateralGrip: number;
  reverseSpeed: number;
}

export type DriftTierName = 'none' | 'blue' | 'orange' | 'purple';
export type DriftBoostTier = Exclude<DriftTierName, 'none'>;

export interface DriftThresholds {
  blue: number;
  orange: number;
  purple: number;
}

export interface DriftBoostProfile {
  duration: number;
  speedMultiplier: number;
}

export const sliceOneDriver: DriverStats = {
  speed: 7,
  acceleration: 7,
  weight: 6,
  handling: 7,
  miniTurbo: 4,
  traction: 5,
};

function normalizedStat(value: number): number {
  return (value - 1) / 9;
}

function clamp01(value: number): number {
  return Math.min(1, Math.max(0, value));
}

function lerp(from: number, to: number, amount: number): number {
  return from + (to - from) * amount;
}

export function createKartTuning(stats: DriverStats): KartTuning {
  return {
    // Candidate F keeps the accepted Speed-7 ceiling at 29.5 m/s and uses a
    // 3.0 m/s Speed 1-10 spread. Candidate G preserves that character-balance
    // mapping while correcting player-vs-AI race execution.
    maxSpeed: 27.5 + normalizedStat(stats.speed) * 3,
    acceleration: 4 + 0.55 * stats.acceleration,
    mass: 105 + normalizedStat(stats.weight) * 75,
    steeringRate: 1.3 + normalizedStat(stats.handling) * 1.1,
    lateralGrip: 5.5 + normalizedStat(stats.traction) * 3.5,
    reverseSpeed: 8,
  };
}

export function handlingCornerSpeedMultiplier(
  handling: number,
  steeringMagnitude: number,
): number {
  const handlingN = normalizedStat(handling);
  const severity = Math.min(1, Math.max(0, (Math.abs(steeringMagnitude) - 0.18) / 0.82));
  const fullSteerLoss = 0.2 - 0.13 * handlingN;
  return 1 - fullSteerLoss * severity * severity;
}

export function aiCornerTargetSpeed(
  characterMaxSpeed: number,
  pace: number,
  corner: number,
  speedLimitMultiplier: number,
  handling: number,
): number {
  // Candidate G keeps AI anticipation modest because the shared controller
  // already applies Handling-based physical corner-speed loss to both player
  // and AI karts. The former 34-48% AI-only corner penalty compounded that
  // shared limit and made a competent player effectively unreachable.
  const baseCornerPenalty = lerp(0.1, 0.04, clamp01(pace));
  const handlingPenaltyFactor = lerp(1.04, 0.96, clamp01(normalizedStat(handling)));
  const cornerPenalty = baseCornerPenalty * handlingPenaltyFactor;
  return (
    characterMaxSpeed *
    (1 - clamp01(corner) * cornerPenalty) *
    Math.min(1.04, Math.max(1, speedLimitMultiplier))
  );
}

export function aiRequestedDriftTier(
  steering: number,
  cornerDemand: number,
  speed: number,
  aggression: number,
  miniTurbo: number,
): DriftBoostTier | undefined {
  const turboN = clamp01(normalizedStat(miniTurbo));
  const demand = Math.max(Math.abs(steering), clamp01(cornerDemand));
  const minimumSpeed = lerp(13, 10.5, turboN);
  const demandGate = lerp(0.68, 0.58, turboN);
  const aggressionGate = lerp(0.38, 0.24, turboN);
  const effectiveAggression = clamp01(aggression + 0.1 * turboN);
  if (speed <= minimumSpeed || demand <= demandGate || effectiveAggression <= aggressionGate) {
    return undefined;
  }

  const purpleDemand = lerp(0.82, 0.76, turboN);
  const orangeDemand = lerp(0.72, 0.66, turboN);
  if (demand >= purpleDemand && effectiveAggression >= 0.48) return 'purple';
  if (demand >= orangeDemand && effectiveAggression >= 0.36) return 'orange';
  return 'blue';
}

export function surfaceSpeedMultiplier(surface: SurfaceType, traction: number): number {
  const tractionN = normalizedStat(traction);
  switch (surface) {
    case 'dirt': return 0.6 + 0.23 * tractionN;
    case 'grass': return 0.425 + 0.225 * tractionN;
    default: return 1;
  }
}

export function surfaceAccelerationMultiplier(surface: SurfaceType, traction: number): number {
  const tractionN = normalizedStat(traction);
  switch (surface) {
    case 'dirt': return 0.68 + 0.22 * tractionN;
    case 'grass': return 0.585 + 0.205 * tractionN;
    default: return 1;
  }
}

export function surfaceMinimumPlayableSpeed(surface: SurfaceType): number {
  if (surface === 'grass') return 8.5;
  if (surface === 'dirt') return 11.5;
  return 0;
}

export function driftThresholds(miniTurbo: number): DriftThresholds {
  const turboN = normalizedStat(miniTurbo);
  return { blue: 0.95 - 0.18 * turboN, orange: 1.9 - 0.35 * turboN, purple: 3.15 - 0.6 * turboN };
}

export function driftBoostProfile(tier: DriftBoostTier, miniTurbo: number): DriftBoostProfile {
  const turboN = normalizedStat(miniTurbo);
  if (tier === 'blue') return { duration: 0.55 + 0.15 * turboN, speedMultiplier: 1.08 };
  if (tier === 'orange') return { duration: 0.9 + 0.25 * turboN, speedMultiplier: 1.12 };
  return { duration: 1.35 + 0.4 * turboN, speedMultiplier: 1.16 };
}

export function aiDriftTargetTier(requestedTier: DriftBoostTier, miniTurbo: number): DriftBoostTier {
  if (miniTurbo <= 4) return 'blue';
  if (miniTurbo <= 7 && requestedTier === 'purple') return 'orange';
  return requestedTier;
}
