import { open, readFile } from 'node:fs/promises';
import { inflateSync } from 'node:zlib';

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
  'public/assets/characters/aa-05/kart.glb',
  'public/assets/characters/aa-05/kart-lod1.glb',
  'public/assets/characters/aa-05/kart-lod2.glb',
  'public/assets/characters/aa-10/kart.glb',
  'public/assets/characters/aa-10/kart-lod1.glb',
  'public/assets/characters/aa-10/kart-lod2.glb',
  'public/assets/characters/aa-04/kart.glb',
  'public/assets/characters/aa-04/kart-lod1.glb',
  'public/assets/characters/aa-04/kart-lod2.glb',
  'public/assets/characters/aa-07/kart.glb',
  'public/assets/characters/aa-07/kart-lod1.glb',
  'public/assets/characters/aa-07/kart-lod2.glb',
  'public/assets/characters/aa-08/kart.glb',
  'public/assets/characters/aa-08/kart-lod1.glb',
  'public/assets/characters/aa-08/kart-lod2.glb',
  'public/assets/characters/aa-03/kart.glb',
  'public/assets/characters/aa-03/kart-lod1.glb',
  'public/assets/characters/aa-03/kart-lod2.glb',
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

const runtimePngs = [
  ['public/assets/characters/aa-04/portrait.png', 256, 256],
  ['public/assets/characters/aa-04/driver/front.png', 512, 512],
  ['public/assets/characters/aa-04/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-04/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-04/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-04/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-04/driver/victory.png', 512, 512],
  ['public/assets/characters/aa-07/portrait.png', 256, 256],
  ['public/assets/characters/aa-07/driver/front.png', 512, 512],
  ['public/assets/characters/aa-07/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-07/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-07/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-07/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-07/driver/victory.png', 512, 512],
  ['public/assets/characters/aa-08/portrait.png', 256, 256],
  ['public/assets/characters/aa-08/driver/front.png', 512, 512],
  ['public/assets/characters/aa-08/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-08/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-08/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-08/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-08/driver/victory.png', 512, 512],
  ['public/assets/characters/aa-03/portrait.png', 256, 256],
  ['public/assets/characters/aa-03/driver/front.png', 512, 512],
  ['public/assets/characters/aa-03/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-03/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-03/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-03/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-03/driver/victory.png', 512, 512],
];

for (const [path, expectedWidth, expectedHeight] of runtimePngs) {
  const png = await readFile(path);
  if (!png.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) {
    throw new Error(`${path} does not have a valid PNG signature.`);
  }

  let offset = 8;
  let width;
  let height;
  const compressed = [];
  while (offset + 12 <= png.length) {
    const length = png.readUInt32BE(offset);
    const type = png.subarray(offset + 4, offset + 8).toString('ascii');
    const dataStart = offset + 8;
    const dataEnd = dataStart + length;
    if (dataEnd + 4 > png.length) throw new Error(`${path} contains a truncated ${type} chunk.`);
    const data = png.subarray(dataStart, dataEnd);
    if (type === 'IHDR') {
      width = data.readUInt32BE(0);
      height = data.readUInt32BE(4);
      if (data[8] !== 8 || data[9] !== 6 || data[12] !== 0) {
        throw new Error(`${path} must be non-interlaced 8-bit RGBA PNG data.`);
      }
    } else if (type === 'IDAT') {
      compressed.push(data);
    }
    offset = dataEnd + 4;
    if (type === 'IEND') break;
  }

  if (width !== expectedWidth || height !== expectedHeight) {
    throw new Error(`${path} must be ${String(expectedWidth)}x${String(expectedHeight)}.`);
  }
  const pixels = inflateSync(Buffer.concat(compressed));
  const rowLength = width * 4 + 1;
  if (pixels.length !== rowLength * height) throw new Error(`${path} has incomplete pixel data.`);
  for (let row = 0; row < height; row += 1) {
    const filter = pixels[row * rowLength];
    if (filter > 4)
      throw new Error(`${path} has invalid PNG filter ${String(filter)} on row ${String(row)}.`);
  }
}

console.log(`Decoded and verified ${String(runtimePngs.length)} runtime character PNGs.`);
