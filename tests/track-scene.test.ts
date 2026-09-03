import { describe, expect, it } from 'vitest';
import * as THREE from 'three';
import { CircuitAlpha } from '../src/game/track/CircuitAlpha';
import { createTrackScene } from '../src/game/track/createTrackScene';

function requireInstanced(scene: THREE.Object3D, name: string): THREE.InstancedMesh {
  const object = scene.getObjectByName(name);
  expect(object).toBeInstanceOf(THREE.InstancedMesh);
  return object as THREE.InstancedMesh;
}

describe('Circuit Alpha environment scene', () => {
  it('adds the visual-landmark pass without mutating canonical track samples', () => {
    const track = new CircuitAlpha();
    const before = track.samples.map((point) => point.toArray());
    const scene = createTrackScene(track);

    expect(scene.name).toBe('circuit-alpha-environment');
    expect(scene.getObjectByName('track-road')).toBeDefined();
    expect(scene.getObjectByName('track-shoulder')).toBeDefined();
    expect(scene.getObjectByName('asphalt-racing-wear')).toBeDefined();
    expect(scene.getObjectByName('split-bend-dirt-line')).toBeDefined();
    expect(scene.getObjectByName('center-mesa')).toBeDefined();
    expect(scene.getObjectByName('start-finish-gate')).toBeDefined();
    expect(scene.getObjectByName('underpass-gate')).toBeDefined();
    expect(scene.getObjectByName('crest-ramp-visual')).toBeDefined();
    expect(scene.getObjectByName('boost-pad-0.450')).toBeDefined();
    expect(scene.getObjectByName('boost-pad-0.815')).toBeDefined();
    expect(track.samples.map((point) => point.toArray())).toEqual(before);
  });

  it('keeps the Crest Ramp long axis aligned to the track-local forward axis', () => {
    const scene = createTrackScene(new CircuitAlpha());
    const deck = scene.getObjectByName('crest-ramp-deck');
    expect(deck).toBeInstanceOf(THREE.Mesh);
    const geometry = (deck as THREE.Mesh).geometry as THREE.BoxGeometry;
    expect(geometry.parameters.depth).toBeGreaterThan(geometry.parameters.width);
  });

  it('uses instancing for repeated trackside dressing', () => {
    const scene = createTrackScene(new CircuitAlpha());

    expect(requireInstanced(scene, 'roadside-curbs').count).toBeGreaterThanOrEqual(90);
    expect(requireInstanced(scene, 'roadside-reflectors').count).toBeGreaterThanOrEqual(48);
    expect(requireInstanced(scene, 'forest-trunks').count).toBe(64);
    expect(requireInstanced(scene, 'forest-canopy').count).toBe(64);
    expect(requireInstanced(scene, 'trackside-rocks').count).toBe(36);
    expect(requireInstanced(scene, 'distant-mountains').count).toBe(18);
    expect(requireInstanced(scene, 'checkpoint-pylons').count).toBe(24);
  });
});
