import * as THREE from 'three';

export class ChaseCamera {
  private readonly desired = new THREE.Vector3();
  private readonly lookAt = new THREE.Vector3();

  public constructor(private readonly camera: THREE.PerspectiveCamera) {}

  public update(
    kartPosition: THREE.Vector3,
    kartForward: THREE.Vector3,
    rearView: boolean,
    dt: number,
  ): void {
    const direction = kartForward.clone().multiplyScalar(rearView ? 1 : -1);
    this.desired
      .copy(kartPosition)
      .addScaledVector(direction, 9)
      .add(new THREE.Vector3(0, 5.2, 0));
    this.camera.position.lerp(this.desired, 1 - Math.exp(-7 * dt));
    this.lookAt
      .copy(kartPosition)
      .addScaledVector(kartForward, rearView ? -7 : 6)
      .setY(1.1);
    this.camera.lookAt(this.lookAt);
  }
}
