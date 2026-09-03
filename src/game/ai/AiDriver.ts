import * as THREE from 'three';
import type { DriftBoostTier } from '../../config/kartTuning';
import type { DriveInput } from '../physics/KartController';
import type { CircuitAlpha } from '../track/CircuitAlpha';

export interface AiDriverProfile {
  laneOffset: number;
  pace: number;
  aggression: number;
}

export interface AiRacerAwareness {
  position: THREE.Vector3;
  speed: number;
  lateralOffset: number;
}

interface NearbyRacer {
  forwardGap: number;
  lateralOffset: number;
  speed: number;
}

const candidateLaneOffsets = [-3.3, -1.65, 0, 1.65, 3.3] as const;

export function aiLookaheadMeters(speed: number): number {
  return THREE.MathUtils.lerp(5, 14, THREE.MathUtils.clamp(speed / 30, 0, 1));
}

export function rubberBandFactor(progressDelta: number): number {
  return THREE.MathUtils.clamp(1 + Math.max(0, progressDelta) * 0.025, 1, 1.04);
}

export function aiTargetSpeed(
  characterMaxSpeed: number,
  pace: number,
  corner: number,
  playerProgressDelta: number,
): number {
  const cornerPenalty = THREE.MathUtils.lerp(0.48, 0.34, THREE.MathUtils.clamp(pace, 0, 1));
  return (
    characterMaxSpeed *
    (1 - THREE.MathUtils.clamp(corner, 0, 1) * cornerPenalty) *
    rubberBandFactor(playerProgressDelta)
  );
}

export function aiRequestedDriftTier(
  steering: number,
  speed: number,
  aggression: number,
): DriftBoostTier | undefined {
  const steeringMagnitude = Math.abs(steering);
  if (speed <= 11 || steeringMagnitude <= 0.62 || aggression <= 0.35) return undefined;
  if (steeringMagnitude >= 0.82 && aggression >= 0.55) return 'purple';
  if (steeringMagnitude >= 0.7 && aggression >= 0.4) return 'orange';
  return 'blue';
}

export class AiDriver {
  private laneOffset: number;
  private laneHoldSeconds = 0;

  public constructor(
    private readonly track: CircuitAlpha,
    private readonly profile: AiDriverProfile,
    private readonly characterMaxSpeed: number,
  ) {
    this.laneOffset = this.roadBoundedLane(profile.laneOffset);
  }

  public input(
    position: THREE.Vector3,
    forward: THREE.Vector3,
    speed: number,
    playerProgressDelta = 0,
    nearbyRacers: readonly AiRacerAwareness[] = [],
    dt = 1 / 60,
  ): DriveInput {
    const projection = this.track.project(position);
    const racersAhead = this.racersAhead(position, projection.tangent, nearbyRacers);
    this.updateLane(racersAhead, speed, dt);

    const lookahead = Math.max(1, Math.round(aiLookaheadMeters(speed) / this.track.sampleSpacing));
    const targetIndex = (projection.index + lookahead) % this.track.sampleCount;
    const target = this.track.samples[targetIndex]?.clone() ?? projection.point.clone();
    const tangent = this.track.tangents[targetIndex]?.clone() ?? projection.tangent.clone();
    const right = new THREE.Vector3(tangent.z, 0, -tangent.x);
    const laneWave =
      Math.sin(projection.progress * Math.PI * 8 + this.profile.aggression * 4) * 0.16;
    target.addScaledVector(right, this.roadBoundedLane(this.laneOffset + laneWave));

    const desired = target.sub(position).setY(0).normalize();
    const cross = forward.z * desired.x - forward.x * desired.z;
    const steering = THREE.MathUtils.clamp(cross * 2.6, -1, 1);
    const corner = 1 - Math.max(0, forward.dot(tangent));
    let targetSpeed = aiTargetSpeed(
      this.characterMaxSpeed,
      this.profile.pace,
      corner,
      playerProgressDelta,
    );
    const blocker = racersAhead.find(
      (racer) => racer.forwardGap < 5.5 && Math.abs(racer.lateralOffset - this.laneOffset) < 1.5,
    );
    if (blocker !== undefined) targetSpeed = Math.min(targetSpeed, blocker.speed + 0.4);

    const driftTarget = aiRequestedDriftTier(steering, speed, this.profile.aggression);
    const input: DriveInput = {
      throttle: speed < targetSpeed ? 1 : 0.2,
      steering,
      brake: speed > targetSpeed + 2,
      drift: driftTarget !== undefined,
      speedLimitMultiplier: rubberBandFactor(playerProgressDelta),
    };
    if (driftTarget !== undefined) input.aiDriftTarget = driftTarget;
    return input;
  }

  public desiredLaneOffset(): number {
    return this.laneOffset;
  }

  private racersAhead(
    position: THREE.Vector3,
    tangent: THREE.Vector3,
    racers: readonly AiRacerAwareness[],
  ): NearbyRacer[] {
    return racers
      .map((racer) => {
        const relative = racer.position.clone().sub(position).setY(0);
        return {
          forwardGap: relative.dot(tangent),
          lateralOffset: racer.lateralOffset,
          speed: racer.speed,
        };
      })
      .filter((racer) => racer.forwardGap > 0.5 && racer.forwardGap < 18)
      .sort((a, b) => a.forwardGap - b.forwardGap);
  }

  private updateLane(racersAhead: readonly NearbyRacer[], speed: number, dt: number): void {
    this.laneHoldSeconds = Math.max(0, this.laneHoldSeconds - dt);
    if (this.laneHoldSeconds > 0) return;

    const preferredLane = this.roadBoundedLane(this.profile.laneOffset);
    const blocker = racersAhead.find(
      (racer) =>
        racer.forwardGap < 14 &&
        Math.abs(racer.lateralOffset - this.laneOffset) < 1.65 &&
        speed > 8 &&
        (speed > racer.speed + 0.35 || racer.forwardGap < 4),
    );

    if (blocker === undefined) {
      if (Math.abs(this.laneOffset - preferredLane) > 0.1) {
        this.laneOffset = preferredLane;
        this.laneHoldSeconds = 0.8;
      }
      return;
    }

    const currentScore = this.laneScore(this.laneOffset, preferredLane, racersAhead);
    let bestLane = this.laneOffset;
    let bestScore = currentScore;
    for (const candidate of candidateLaneOffsets) {
      const score = this.laneScore(candidate, preferredLane, racersAhead);
      if (score < bestScore) {
        bestLane = candidate;
        bestScore = score;
      }
    }

    if (currentScore - bestScore > 0.8) {
      this.laneOffset = this.roadBoundedLane(bestLane);
      this.laneHoldSeconds = THREE.MathUtils.lerp(2.1, 1.35, this.profile.aggression);
    }
  }

  private laneScore(
    candidate: number,
    preferredLane: number,
    racersAhead: readonly NearbyRacer[],
  ): number {
    let score = Math.abs(candidate - preferredLane) * 0.3;
    for (const racer of racersAhead) {
      const clearance = Math.abs(candidate - racer.lateralOffset);
      if (clearance >= 2.1) continue;
      score += (2.1 - clearance) * (18 - racer.forwardGap) * 0.85;
    }
    return score;
  }

  private roadBoundedLane(offset: number): number {
    const kartMargin = 1.4;
    return THREE.MathUtils.clamp(
      offset,
      -this.track.roadHalfWidth + kartMargin,
      this.track.roadHalfWidth - kartMargin,
    );
  }
}
