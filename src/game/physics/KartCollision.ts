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
