export interface CollisionImpulseShares {
  first: number;
  second: number;
}

export function collisionImpulseShares(
  firstMass: number,
  secondMass: number,
  totalStrength: number,
): CollisionImpulseShares {
  const totalMass = Math.max(firstMass + secondMass, 1);
  return {
    first: totalStrength * (secondMass / totalMass),
    second: totalStrength * (firstMass / totalMass),
  };
}

function clamp(value: number, minimum: number, maximum: number): number {
  return Math.min(maximum, Math.max(minimum, value));
}

export function collisionSpeedRetention(
  weight: number,
  otherWeight: number,
  closingSpeed: number,
): number {
  if (closingSpeed < 0.75) return 1;

  const normalizedWeight = clamp((weight - 1) / 9, 0, 1);
  const fullImpactLoss = 0.31 + (0.16 - 0.31) * normalizedWeight;
  const impactSeverity = clamp(closingSpeed / 16, 0.25, 1);
  const opponentPressure = clamp(1 + 0.015 * (otherWeight - weight), 0.86, 1.14);
  return clamp(1 - fullImpactLoss * impactSeverity * opponentPressure, 0.65, 0.96);
}
