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

export const sliceOneDriver: DriverStats = {
  speed: 7,
  acceleration: 7,
  weight: 6,
  handling: 7,
  miniTurbo: 4,
  traction: 5,
};

export function createKartTuning(stats: DriverStats): KartTuning {
  const normalized = (value: number): number => (value - 1) / 9;

  return {
    maxSpeed: 23 + normalized(stats.speed) * 10,
    acceleration: 14 + normalized(stats.acceleration) * 10,
    mass: 105 + normalized(stats.weight) * 75,
    steeringRate: 1.3 + normalized(stats.handling) * 1.1,
    lateralGrip: 5.5 + normalized(stats.traction) * 3.5,
    reverseSpeed: 8,
  };
}

export function surfaceSpeedMultiplier(surface: SurfaceType, traction: number): number {
  const tractionN = (traction - 1) / 9;

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
  const tractionN = (traction - 1) / 9;

  switch (surface) {
    case 'dirt':
      return 0.68 + 0.22 * tractionN;
    case 'grass':
      return 0.585 + 0.205 * tractionN;
    default:
      return 1;
  }
}
