import { open } from 'node:fs/promises';

const runtimeGlbs = [
  'public/assets/characters/aa-02/kart.glb',
  'public/assets/characters/aa-02/kart-lod1.glb',
  'public/assets/characters/aa-02/kart-lod2.glb',
];

for (const path of runtimeGlbs) {
  const file = await open(path, 'r');
  try {
    const signature = Buffer.alloc(4);
    await file.read(signature, 0, signature.length, 0);
    if (signature.toString('ascii') !== 'glTF') {
      throw new Error(`${path} is not a materialized GLB. Check Git LFS checkout.`);
    }
  } finally {
    await file.close();
  }
}

console.log(`Verified ${String(runtimeGlbs.length)} materialized runtime GLBs.`);
