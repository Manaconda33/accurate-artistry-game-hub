import * as THREE from 'three';
import { CircuitAlpha } from './CircuitAlpha';

function createStrip(
  track: CircuitAlpha,
  halfWidth: number,
  material: THREE.Material,
  y: number,
): THREE.Mesh {
  const positions: number[] = [];
  const indices: number[] = [];

  for (let index = 0; index <= track.sampleCount; index += 1) {
    const wrapped = index % track.sampleCount;
    const point = track.samples[wrapped]?.clone() ?? new THREE.Vector3();
    const tangent = track.tangents[wrapped] ?? new THREE.Vector3(0, 0, 1);
    const right = new THREE.Vector3(tangent.z, 0, -tangent.x).normalize();
    const leftPoint = point.clone().addScaledVector(right, -halfWidth);
    const rightPoint = point.clone().addScaledVector(right, halfWidth);
    positions.push(leftPoint.x, y, leftPoint.z, rightPoint.x, y, rightPoint.z);

    if (index < track.sampleCount) {
      const base = index * 2;
      indices.push(base, base + 2, base + 1, base + 1, base + 2, base + 3);
    }
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  return new THREE.Mesh(geometry, material);
}

function markerAt(track: CircuitAlpha, progress: number, color: number): THREE.Mesh {
  const point = track.curve.getPointAt(progress);
  const tangent = track.curve.getTangentAt(progress);
  const marker = new THREE.Mesh(
    new THREE.BoxGeometry(9, 0.14, 3.2),
    new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.35 }),
  );
  marker.position.copy(point).setY(0.12);
  marker.rotation.y = Math.atan2(tangent.x, tangent.z);
  return marker;
}

function createSegmentStrip(
  track: CircuitAlpha,
  startProgress: number,
  endProgress: number,
  centerOffset: number,
  halfWidth: number,
  material: THREE.Material,
  y: number,
): THREE.Mesh {
  const positions: number[] = [];
  const indices: number[] = [];
  const start = Math.floor(startProgress * track.sampleCount);
  const end = Math.ceil(endProgress * track.sampleCount);

  for (let index = start; index <= end; index += 1) {
    const wrapped = index % track.sampleCount;
    const point = track.samples[wrapped]?.clone() ?? new THREE.Vector3();
    const tangent = track.tangents[wrapped] ?? new THREE.Vector3(0, 0, 1);
    const right = new THREE.Vector3(tangent.z, 0, -tangent.x).normalize();
    const center = point.addScaledVector(right, centerOffset);
    const leftPoint = center.clone().addScaledVector(right, -halfWidth);
    const rightPoint = center.clone().addScaledVector(right, halfWidth);
    positions.push(leftPoint.x, y, leftPoint.z, rightPoint.x, y, rightPoint.z);
    const local = index - start;
    if (index < end) {
      const base = local * 2;
      indices.push(base, base + 2, base + 1, base + 1, base + 2, base + 3);
    }
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  return new THREE.Mesh(geometry, material);
}

function createSky(): THREE.Mesh {
  return new THREE.Mesh(
    new THREE.SphereGeometry(760, 32, 18),
    new THREE.ShaderMaterial({
      side: THREE.BackSide,
      depthWrite: false,
      uniforms: {
        topColor: { value: new THREE.Color(0x3b2d67) },
        horizonColor: { value: new THREE.Color(0xe1a7bd) },
        lowerColor: { value: new THREE.Color(0x796481) },
      },
      vertexShader: `varying vec3 worldPosition;
        void main() {
          vec4 world = modelMatrix * vec4(position, 1.0);
          worldPosition = world.xyz;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }`,
      fragmentShader: `uniform vec3 topColor;
        uniform vec3 horizonColor;
        uniform vec3 lowerColor;
        varying vec3 worldPosition;
        void main() {
          float h = normalize(worldPosition).y;
          vec3 color = h >= 0.0
            ? mix(horizonColor, topColor, smoothstep(0.0, 0.72, h))
            : mix(horizonColor, lowerColor, smoothstep(0.0, -0.35, h));
          gl_FragColor = vec4(color, 1.0);
        }`,
    }),
  );
}

export function createTrackScene(track: CircuitAlpha): THREE.Group {
  const group = new THREE.Group();
  group.add(createSky());

  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(900, 900),
    new THREE.MeshStandardMaterial({ color: 0x294e35, roughness: 1 }),
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.08;
  ground.receiveShadow = true;
  group.add(ground);

  const road = createStrip(
    track,
    track.roadHalfWidth,
    new THREE.MeshStandardMaterial({ color: 0x30313b, roughness: 0.88 }),
    0,
  );
  road.receiveShadow = true;
  group.add(road);

  const shoulder = createStrip(
    track,
    track.roadHalfWidth + 0.65,
    new THREE.MeshStandardMaterial({ color: 0xb69bd8, roughness: 0.9 }),
    -0.02,
  );
  group.add(shoulder);
  group.remove(road);
  group.add(shoulder, road);

  const dirt = createSegmentStrip(
    track,
    0.235,
    0.315,
    3.75,
    2.25,
    new THREE.MeshStandardMaterial({ color: 0x8b5938, roughness: 1 }),
    0.025,
  );
  group.add(dirt);

  group.add(markerAt(track, 0.45, 0x29c9ff), markerAt(track, 0.815, 0x29c9ff));

  const ramp = markerAt(track, 0.5, 0xf1c65b);
  ramp.scale.z = 1.8;
  ramp.rotation.x = -THREE.MathUtils.degToRad(7);
  group.add(ramp);

  track.checkpointIndices.forEach((sampleIndex, checkpointIndex) => {
    const point = track.samples[sampleIndex] ?? new THREE.Vector3();
    const tangent = track.tangents[sampleIndex] ?? new THREE.Vector3(0, 0, 1);
    const postMaterial = new THREE.MeshStandardMaterial({
      color: checkpointIndex === 0 ? 0xf5e66a : 0x6d4a86,
      emissive: checkpointIndex === 0 ? 0x554900 : 0x170c22,
    });
    const right = new THREE.Vector3(tangent.z, 0, -tangent.x);
    for (const side of [-1, 1]) {
      const post = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.38, 3.2, 8), postMaterial);
      post.position.copy(point).addScaledVector(right, side * (track.roadHalfWidth + 1));
      post.position.y = 1.6;
      group.add(post);
    }
  });

  const center = new THREE.Mesh(
    new THREE.CylinderGeometry(62, 80, 24, 10),
    new THREE.MeshStandardMaterial({ color: 0x432b58, roughness: 0.82 }),
  );
  center.position.y = 12;
  group.add(center);

  return group;
}
