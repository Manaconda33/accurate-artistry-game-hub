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

export function createKartTuning(stats: DriverStats): KartTuning {
  return {
    // Candidate A compresses the Speed 1-10 spread from 10 m/s to 6 m/s.
    // Speed remains authoritative for sustained straight-line velocity while
    // reducing how much one Speed point can overwhelm the other five stats.
    maxSpeed: 25.5 + normalizedStat(stats.speed) * 6,
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
  const fullSteerLoss = 0.18 - 0.12 * handlingN;
  return 1 - fullSteerLoss * severity * severity;
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
