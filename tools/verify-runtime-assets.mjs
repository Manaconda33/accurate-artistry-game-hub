import { open } from 'node:fs/promises';

const runtimeGlbs = [
  'public/assets/characters/aa-02/kart.glb',
  'public/assets/characters/aa-02/kart-lod1.glb',
  'public/assets/characters/aa-02/kart-lod2.glb',
  'public/assets/characters/aa-09/kart.glb',
  'public/assets/characters/aa-09/kart-lod1.glb',
  'public/assets/characters/aa-09/kart-lod2.glb',
  'public/assets/characters/aa-11/kart.glb',
  'public/assets/characters/aa-11/kart-lod1.glb',
  'public/assets/characters/aa-11/kart-lod2.glb',
];

for (const path of runtimeGlbs) {
  const file = await open(path, 'r');
  try {
    const signature = Buffer.alloc(4);
    await file.read(signature, 0, signature.length, 0);
    if (signature.toString('ascii') !== 'glTF') {
      throw new Error(`${path} is not a materialized GLB. Check Git LFS checkout.`);
    }
    const chunkHeader = Buffer.alloc(8);
    await file.read(chunkHeader, 0, chunkHeader.length, 12);
    const jsonLength = chunkHeader.readUInt32LE(0);
    if (chunkHeader.subarray(4).toString('ascii') !== 'JSON') {
      throw new Error(`${path} does not begin with a glTF JSON chunk.`);
    }
    const jsonChunk = Buffer.alloc(jsonLength);
    await file.read(jsonChunk, 0, jsonLength, 20);
    const gltf = JSON.parse(jsonChunk.toString('utf8'));
    if (gltf.extras?.forward !== '-Z') {
      throw new Error(`${path} must declare extras.forward as -Z.`);
    }
  } finally {
    await file.close();
  }
}

console.log(`Verified ${String(runtimeGlbs.length)} materialized runtime GLBs.`);
