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
    // Candidate B+ keeps the accepted Speed-7 ceiling at 29.5 m/s while
    // compressing the full Speed 1-10 spread to 3 m/s. Speed remains the
    // authoritative sustained straight-line stat without overwhelming the
    // other five equal-budget attributes on Circuit Alpha.
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
  // Candidate B+ makes Handling a real pace stat in technical sections while
  // leaving straight-line ceilings unchanged. At full steering demand the
  // governed speed loss spans 25% at Handling 1 to 5% at Handling 10.
  const fullSteerLoss = 0.25 - 0.2 * handlingN;
  return 1 - fullSteerLoss * severity * severity;
}

export function aiCornerTargetSpeed(
  characterMaxSpeed: number,
  pace: number,
  corner: number,
  speedLimitMultiplier: number,
  handling: number,
): number {
  const baseCornerPenalty = lerp(0.48, 0.34, clamp01(pace));
  const handlingPenaltyFactor = lerp(1.2, 0.72, clamp01(normalizedStat(handling)));
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
  // The lookahead turn angle is a better drift-opportunity signal than raw
  // spline steering alone. High Mini-Turbo lowers the demand/speed gates and
  // raises effective aggression, so those builds deliberately exploit more
  // corners while low-Mini-Turbo builds remain selective.
  const demand = Math.max(Math.abs(steering), clamp01(cornerDemand));
  const minimumSpeed = lerp(13, 9.5, turboN);
  const demandGate = lerp(0.68, 0.54, turboN);
  const aggressionGate = lerp(0.38, 0.18, turboN);
  const effectiveAggression = clamp01(aggression + 0.18 * turboN);
  if (speed <= minimumSpeed || demand <= demandGate || effectiveAggression <= aggressionGate) {
    return undefined;
  }

  const purpleDemand = lerp(0.82, 0.74, turboN);
  const orangeDemand = lerp(0.72, 0.64, turboN);
  if (demand >= purpleDemand && effectiveAggression >= 0.48) return 'purple';
  if (demand >= orangeDemand && effectiveAggression >= 0.36) return 'orange';
  return 'blue';
}

export function surfaceSpeedMultiplier(surface: SurfaceType, traction: number): number {
  const tractionN = normalizedStat(traction);

  switch (surface) {
    case 'dirt':
      return 0.6 + 0.23 * tractionN;
    case 'grass':
      return 0.425 + 0.225 * tractionN;
    default:
      return 1;
  }
}

export function surfaceAccelerationMultiplier(surface: SurfaceType, traction: number): number {
  const tractionN = normalizedStat(traction);

  switch (surface) {
    case 'dirt':
      return 0.68 + 0.22 * tractionN;
    case 'grass':
      return 0.585 + 0.205 * tractionN;
    default:
      return 1;
  }
}

export function surfaceMinimumPlayableSpeed(surface: SurfaceType): number {
  if (surface === 'grass') return 8.5;
  if (surface === 'dirt') return 11.5;
  return 0;
}

export function driftThresholds(miniTurbo: number): DriftThresholds {
  const turboN = normalizedStat(miniTurbo);
  return {
    blue: 0.95 - 0.18 * turboN,
    orange: 1.9 - 0.35 * turboN,
    purple: 3.15 - 0.6 * turboN,
  };
}

export function driftBoostProfile(
  tier: DriftBoostTier,
  miniTurbo: number,
): DriftBoostProfile {
  const turboN = normalizedStat(miniTurbo);
  if (tier === 'blue') return { duration: 0.55 + 0.15 * turboN, speedMultiplier: 1.08 };
  if (tier === 'orange') return { duration: 0.9 + 0.25 * turboN, speedMultiplier: 1.12 };
  return { duration: 1.35 + 0.4 * turboN, speedMultiplier: 1.16 };
}

export function aiDriftTargetTier(
  requestedTier: DriftBoostTier,
  miniTurbo: number,
): DriftBoostTier {
  if (miniTurbo <= 4) return 'blue';
  if (miniTurbo <= 7 && requestedTier === 'purple') return 'orange';
  return requestedTier;
}
