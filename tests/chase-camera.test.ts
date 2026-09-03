import { describe, expect, it } from 'vitest';
import * as THREE from 'three';
import { ChaseCamera } from '../src/game/camera/ChaseCamera';

function advance(cameraRig: ChaseCamera, seconds: number, rearView = false): void {
  const position = new THREE.Vector3(0, 0, 0);
  const forward = new THREE.Vector3(0, 0, 1);
  const step = 1 / 60;
  const frames = Math.ceil(seconds / step);
  for (let frame = 0; frame < frames; frame += 1) {
    cameraRig.update(position, forward, rearView, step);
  }
}

describe('race camera presentation', () => {
  it('cranes down from an elevated grid view into the lower chase position', () => {
    const camera = new THREE.PerspectiveCamera();
    const rig = new ChaseCamera(camera);
    const position = new THREE.Vector3(0, 0, 0);
    const forward = new THREE.Vector3(0, 0, 1);

    rig.update(position, forward, false, 1 / 60);
    expect(camera.position.y).toBeGreaterThan(12);
    expect(camera.position.z).toBeGreaterThan(-4);

    advance(rig, 3.1);
    expect(camera.position.y).toBeGreaterThan(2.9);
    expect(camera.position.y).toBeLessThan(3.4);
    expect(camera.position.z).toBeLessThan(-7);
  });

  it('keeps the rear camera at a similarly low racing height', () => {
    const camera = new THREE.PerspectiveCamera();
    const rig = new ChaseCamera(camera);

    advance(rig, 3.1);
    rig.update(new THREE.Vector3(), new THREE.Vector3(0, 0, 1), true, 1);

    expect(camera.position.y).toBeGreaterThan(2.8);
    expect(camera.position.y).toBeLessThan(3.4);
    expect(camera.position.z).toBeGreaterThan(6.5);
  });
});
