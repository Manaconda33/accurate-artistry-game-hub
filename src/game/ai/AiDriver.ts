import * as THREE from 'three';
import type { DriveInput } from '../physics/KartController';
import type { CircuitAlpha } from '../track/CircuitAlpha';

export interface AiDriverProfile {
  laneOffset: number;
  pace: number;
  aggression: number;
}

export function rubberBandFactor(progressDelta: number): number {
  return THREE.MathUtils.clamp(1 + progressDelta * 0.025, 0.95, 1.05);
}

export class AiDriver {
  public constructor(
    private readonly track: CircuitAlpha,
    private readonly profile: AiDriverProfile,
  ) {}

  public input(
    position: THREE.Vector3,
    forward: THREE.Vector3,
    speed: number,
    playerProgressDelta = 0,
  ): DriveInput {
    const projection = this.track.project(position);
    const lookahead = Math.round(10 + Math.min(speed, 30) * 0.7);
    const targetIndex = (projection.index + lookahead) % this.track.sampleCount;
    const target = this.track.samples[targetIndex]?.clone() ?? projection.point.clone();
    const tangent = this.track.tangents[targetIndex]?.clone() ?? projection.tangent.clone();
    const right = new THREE.Vector3(tangent.z, 0, -tangent.x);
    const laneWave =
      Math.sin(projection.progress * Math.PI * 8 + this.profile.aggression * 4) * 0.45;
    target.addScaledVector(right, this.profile.laneOffset + laneWave);

    const desired = target.sub(position).setY(0).normalize();
    const cross = forward.z * desired.x - forward.x * desired.z;
    const steering = THREE.MathUtils.clamp(cross * 2.6, -1, 1);
    const corner = 1 - Math.max(0, forward.dot(tangent));
    const targetSpeed =
      (20.5 + this.profile.pace * 5.5) *
      (1 - corner * 0.42) *
      rubberBandFactor(playerProgressDelta);

    return {
      throttle: speed < targetSpeed ? 1 : 0.2,
      steering,
      brake: speed > targetSpeed + 2,
      drift: Math.abs(steering) > 0.62 && speed > 11 && this.profile.aggression > 0.35,
    };
  }
}
