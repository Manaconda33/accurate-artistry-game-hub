import RAPIER from '@dimforge/rapier3d-compat';
import * as THREE from 'three';
import {
  surfaceAccelerationMultiplier,
  surfaceSpeedMultiplier,
  type DriverStats,
  type KartTuning,
  type SurfaceType,
} from '../../config/kartTuning';

export interface DriveInput {
  throttle: number;
  steering: number;
  brake: boolean;
}

export class KartController {
  public readonly body: RAPIER.RigidBody;
  private yaw: number;
  private currentSteer = 0;
  private boostRemaining = 0;

  public constructor(
    private readonly world: RAPIER.World,
    private readonly tuning: KartTuning,
    private readonly stats: DriverStats,
    spawn: THREE.Vector3,
    yaw: number,
  ) {
    this.yaw = yaw;
    this.body = this.world.createRigidBody(
      RAPIER.RigidBodyDesc.dynamic()
        .setTranslation(spawn.x, 1.1, spawn.z)
        .setLinearDamping(0.35)
        .setAngularDamping(5)
        .enabledRotations(false, true, false),
    );
    this.world.createCollider(
      RAPIER.ColliderDesc.cuboid(0.72, 0.34, 1.18)
        .setMass(this.tuning.mass)
        .setFriction(0.55)
        .setRestitution(0.05),
      this.body,
    );
    this.setYaw(yaw);
  }

  public update(input: DriveInput, surface: SurfaceType, dt: number): void {
    const velocity = this.body.linvel();
    const grounded = this.groundContactCount() >= 2;
    const forward = new THREE.Vector3(Math.sin(this.yaw), 0, Math.cos(this.yaw));
    const right = new THREE.Vector3(forward.z, 0, -forward.x);
    const planar = new THREE.Vector3(velocity.x, 0, velocity.z);
    let forwardSpeed = planar.dot(forward);
    const lateralSpeed = planar.dot(right);
    const speedRatio = Math.min(Math.abs(forwardSpeed) / this.tuning.maxSpeed, 1);
    const steeringScale = THREE.MathUtils.lerp(1, 0.48, speedRatio);
    const steeringTarget = input.steering * this.tuning.steeringRate * steeringScale;
    this.currentSteer = THREE.MathUtils.damp(this.currentSteer, steeringTarget, 10, dt);

    if (Math.abs(forwardSpeed) > 0.35) {
      const direction = forwardSpeed >= 0 ? 1 : -0.65;
      this.yaw += this.currentSteer * dt * direction;
    }

    const speedMultiplier = surfaceSpeedMultiplier(surface, this.stats.traction);
    const accelerationMultiplier = surfaceAccelerationMultiplier(surface, this.stats.traction);
    const maxForward = this.tuning.maxSpeed * speedMultiplier;

    if (surface === 'boost' && this.boostRemaining <= 0) this.boostRemaining = 0.8;
    this.boostRemaining = Math.max(0, this.boostRemaining - dt);
    const boostedMax = maxForward * (this.boostRemaining > 0 ? 1.12 : 1);
    const acceleration =
      this.tuning.acceleration * accelerationMultiplier * (this.boostRemaining > 0 ? 1.35 : 1);

    if (input.throttle > 0 && grounded) {
      forwardSpeed = Math.min(boostedMax, forwardSpeed + acceleration * dt);
    } else if (input.throttle < 0 && grounded) {
      forwardSpeed = Math.max(-this.tuning.reverseSpeed, forwardSpeed - acceleration * 0.72 * dt);
    } else {
      forwardSpeed = THREE.MathUtils.damp(forwardSpeed, 0, 0.65, dt);
    }

    if (input.brake) forwardSpeed = THREE.MathUtils.damp(forwardSpeed, 0, 5.5, dt);

    const retainedLateral = THREE.MathUtils.damp(
      lateralSpeed,
      0,
      this.tuning.lateralGrip * (surface === 'grass' ? 0.55 : surface === 'dirt' ? 0.72 : 1),
      dt,
    );
    const nextForward = new THREE.Vector3(Math.sin(this.yaw), 0, Math.cos(this.yaw));
    const nextRight = new THREE.Vector3(nextForward.z, 0, -nextForward.x);
    const nextVelocity = nextForward
      .multiplyScalar(forwardSpeed)
      .add(nextRight.multiplyScalar(retainedLateral));

    this.body.setLinvel({ x: nextVelocity.x, y: velocity.y, z: nextVelocity.z }, true);
    this.setYaw(this.yaw);
  }

  public respawn(position: THREE.Vector3, yaw: number): void {
    this.yaw = yaw;
    this.currentSteer = 0;
    this.boostRemaining = 0;
    this.body.setTranslation({ x: position.x, y: 1.2, z: position.z }, true);
    this.body.setLinvel({ x: 0, y: 0, z: 0 }, true);
    this.body.setAngvel({ x: 0, y: 0, z: 0 }, true);
    this.setYaw(yaw);
  }

  public position(target = new THREE.Vector3()): THREE.Vector3 {
    const translation = this.body.translation();
    return target.set(translation.x, translation.y, translation.z);
  }

  public speedMetersPerSecond(): number {
    const velocity = this.body.linvel();
    return Math.hypot(velocity.x, velocity.z);
  }

  public forward(target = new THREE.Vector3()): THREE.Vector3 {
    return target.set(Math.sin(this.yaw), 0, Math.cos(this.yaw));
  }

  public isFinite(): boolean {
    const p = this.body.translation();
    const v = this.body.linvel();
    return [p.x, p.y, p.z, v.x, v.y, v.z, this.yaw].every(Number.isFinite);
  }

  private setYaw(yaw: number): void {
    const half = yaw / 2;
    this.body.setRotation({ x: 0, y: Math.sin(half), z: 0, w: Math.cos(half) }, true);
  }

  private groundContactCount(): number {
    const position = this.body.translation();
    const cos = Math.cos(this.yaw);
    const sin = Math.sin(this.yaw);
    const offsets = [
      [-0.55, 0.72],
      [0.55, 0.72],
      [-0.55, -0.72],
      [0.55, -0.72],
    ] as const;

    return offsets.reduce((contacts, [localX, localZ]) => {
      const worldX = position.x + localX * cos + localZ * sin;
      const worldZ = position.z - localX * sin + localZ * cos;
      const ray = new RAPIER.Ray({ x: worldX, y: position.y, z: worldZ }, { x: 0, y: -1, z: 0 });
      const hit = this.world.castRay(ray, 1.35, true, undefined, undefined, undefined, this.body);
      return contacts + (hit === null ? 0 : 1);
    }, 0);
  }
}
