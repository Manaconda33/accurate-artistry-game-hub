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

const paethPredictor = (left, above, upperLeft) => {
  const prediction = left + above - upperLeft;
  const leftDistance = Math.abs(prediction - left);
  const aboveDistance = Math.abs(prediction - above);
  const upperLeftDistance = Math.abs(prediction - upperLeft);
  if (leftDistance <= aboveDistance && leftDistance <= upperLeftDistance) return left;
  if (aboveDistance <= upperLeftDistance) return above;
  return upperLeft;
};

const decodeRgbaRows = (filtered, width, height) => {
  const bytesPerPixel = 4;
  const sourceRowLength = width * bytesPerPixel + 1;
  const decoded = Buffer.alloc(width * height * bytesPerPixel);
  for (let row = 0; row < height; row += 1) {
    const filter = filtered[row * sourceRowLength];
    const sourceStart = row * sourceRowLength + 1;
    const targetStart = row * width * bytesPerPixel;
    for (let column = 0; column < width * bytesPerPixel; column += 1) {
      const raw = filtered[sourceStart + column];
      const left = column >= bytesPerPixel ? decoded[targetStart + column - bytesPerPixel] : 0;
      const above = row > 0 ? decoded[targetStart + column - width * bytesPerPixel] : 0;
      const upperLeft =
        row > 0 && column >= bytesPerPixel
          ? decoded[targetStart + column - width * bytesPerPixel - bytesPerPixel]
          : 0;
      let value = raw;
      if (filter === 1) value += left;
      else if (filter === 2) value += above;
      else if (filter === 3) value += Math.floor((left + above) / 2);
      else if (filter === 4) value += paethPredictor(left, above, upperLeft);
      decoded[targetStart + column] = value & 0xff;
    }
  }
  return decoded;
};

const countEnclosedTransparentRegions = (decoded, width, height, minimumPixels) => {
  const visited = new Uint8Array(width * height);
  let qualifyingRegions = 0;
  for (let start = 0; start < width * height; start += 1) {
    if (visited[start] !== 0 || decoded[start * 4 + 3] !== 0) continue;
    const stack = [start];
    visited[start] = 1;
    let pixels = 0;
    let touchesEdge = false;
    while (stack.length > 0) {
      const pixel = stack.pop();
      const x = pixel % width;
      const y = Math.floor(pixel / width);
      pixels += 1;
      touchesEdge ||= x === 0 || y === 0 || x === width - 1 || y === height - 1;
      for (const neighbor of [pixel - width, pixel + width, pixel - 1, pixel + 1]) {
        if (neighbor < 0 || neighbor >= width * height || visited[neighbor] !== 0) continue;
        const neighborX = neighbor % width;
        if (Math.abs(neighborX - x) > 1 || decoded[neighbor * 4 + 3] !== 0) continue;
        visited[neighbor] = 1;
        stack.push(neighbor);
      }
    }
    if (!touchesEdge && pixels >= minimumPixels) qualifyingRegions += 1;
  }
  return qualifyingRegions;
};

const largestPaleNeutralComponentInRects = (decoded, width, height, rects) => {
  const candidate = new Uint8Array(width * height);
  for (const [left, top, right, bottom] of rects) {
    for (let y = top; y < bottom; y += 1) {
      for (let x = left; x < right; x += 1) {
        const pixel = y * width + x;
        const offset = pixel * 4;
        const red = decoded[offset];
        const green = decoded[offset + 1];
        const blue = decoded[offset + 2];
        const alpha = decoded[offset + 3];
        const maximum = Math.max(red, green, blue);
        const minimum = Math.min(red, green, blue);
        if (alpha > 16 && (red + green + blue) / 3 > 85 && maximum - minimum < 45) {
          candidate[pixel] = 1;
        }
      }
    }
  }

  const visited = new Uint8Array(width * height);
  let largest = 0;
  for (let start = 0; start < width * height; start += 1) {
    if (candidate[start] === 0 || visited[start] !== 0) continue;
    const stack = [start];
    visited[start] = 1;
    let pixels = 0;
    while (stack.length > 0) {
      const pixel = stack.pop();
      const x = pixel % width;
      pixels += 1;
      for (const neighbor of [pixel - width, pixel + width, pixel - 1, pixel + 1]) {
        if (neighbor < 0 || neighbor >= width * height || visited[neighbor] !== 0) continue;
        const neighborX = neighbor % width;
        if (Math.abs(neighborX - x) > 1 || candidate[neighbor] === 0) continue;
        visited[neighbor] = 1;
        stack.push(neighbor);
      }
    }
    largest = Math.max(largest, pixels);
  }
  return largest;
};

const lulaProtectedRects = {
  'portrait.png': [82, 66, 180, 170],
  'front.png': [205, 55, 310, 185],
  'victory.png': [300, 82, 400, 205],
  'front-steer-left.png': [280, 45, 395, 165],
  'front-steer-right.png': [105, 40, 235, 165],
  'front-hit.png': [270, 40, 390, 165],
  'front-victory.png': [210, 45, 325, 175],
};

const runtimePngs = [
  ['public/assets/characters/aa-02/driver/front.png', 512, 512],
  ['public/assets/characters/aa-02/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-02/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-02/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-02/driver/front-victory.png', 512, 512],
  ['public/assets/characters/aa-05/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-05/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-05/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-05/driver/front-victory.png', 512, 512],
  ['public/assets/characters/aa-09/driver/front.png', 512, 512],
  ['public/assets/characters/aa-09/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-09/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-09/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-09/driver/front-victory.png', 512, 512],
  ['public/assets/characters/aa-10/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-10/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-10/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-10/driver/front-victory.png', 512, 512],
  ['public/assets/characters/aa-11/driver/front.png', 512, 512],
  ['public/assets/characters/aa-11/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-11/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-11/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-11/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-11/driver/victory.png', 512, 512],
  ['public/assets/characters/aa-11/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-11/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-11/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-11/driver/front-victory.png', 512, 512],
  ['public/assets/characters/aa-04/portrait.png', 256, 256],
  ['public/assets/characters/aa-04/driver/front.png', 512, 512],
  ['public/assets/characters/aa-04/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-04/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-04/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-04/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-04/driver/victory.png', 512, 512],
  ['public/assets/characters/aa-04/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-04/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-04/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-04/driver/front-victory.png', 512, 512],
  ['public/assets/characters/aa-07/portrait.png', 256, 256],
  ['public/assets/characters/aa-07/driver/front.png', 512, 512],
  ['public/assets/characters/aa-07/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-07/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-07/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-07/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-07/driver/victory.png', 512, 512],
  ['public/assets/characters/aa-07/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-07/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-07/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-07/driver/front-victory.png', 512, 512],
  ['public/assets/characters/aa-08/portrait.png', 256, 256],
  ['public/assets/characters/aa-08/driver/front.png', 512, 512],
  ['public/assets/characters/aa-08/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-08/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-08/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-08/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-08/driver/victory.png', 512, 512],
  ['public/assets/characters/aa-08/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-08/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-08/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-08/driver/front-victory.png', 512, 512],
  ['public/assets/characters/aa-03/portrait.png', 256, 256],
  ['public/assets/characters/aa-03/driver/front.png', 512, 512],
  ['public/assets/characters/aa-03/driver/rear.png', 512, 512],
  ['public/assets/characters/aa-03/driver/steer-left.png', 512, 512],
  ['public/assets/characters/aa-03/driver/steer-right.png', 512, 512],
  ['public/assets/characters/aa-03/driver/hit.png', 512, 512],
  ['public/assets/characters/aa-03/driver/victory.png', 512, 512],
  ['public/assets/characters/aa-03/driver/front-steer-left.png', 512, 512],
  ['public/assets/characters/aa-03/driver/front-steer-right.png', 512, 512],
  ['public/assets/characters/aa-03/driver/front-hit.png', 512, 512],
  ['public/assets/characters/aa-03/driver/front-victory.png', 512, 512],
];

const newTransparentFronts = new Set([
  'public/assets/characters/aa-02/driver/front.png',
  'public/assets/characters/aa-02/driver/front-steer-left.png',
  'public/assets/characters/aa-02/driver/front-steer-right.png',
  'public/assets/characters/aa-02/driver/front-hit.png',
  'public/assets/characters/aa-02/driver/front-victory.png',
  'public/assets/characters/aa-05/driver/front-steer-left.png',
  'public/assets/characters/aa-05/driver/front-steer-right.png',
  'public/assets/characters/aa-05/driver/front-hit.png',
  'public/assets/characters/aa-05/driver/front-victory.png',
  'public/assets/characters/aa-09/driver/front.png',
  'public/assets/characters/aa-09/driver/front-steer-left.png',
  'public/assets/characters/aa-09/driver/front-steer-right.png',
  'public/assets/characters/aa-09/driver/front-hit.png',
  'public/assets/characters/aa-09/driver/front-victory.png',
  'public/assets/characters/aa-10/driver/front-steer-left.png',
  'public/assets/characters/aa-10/driver/front-steer-right.png',
  'public/assets/characters/aa-10/driver/front-hit.png',
  'public/assets/characters/aa-10/driver/front-victory.png',
  'public/assets/characters/aa-04/driver/front-steer-left.png',
  'public/assets/characters/aa-04/driver/front-steer-right.png',
  'public/assets/characters/aa-04/driver/front-hit.png',
  'public/assets/characters/aa-04/driver/front-victory.png',
  'public/assets/characters/aa-07/driver/front-steer-left.png',
  'public/assets/characters/aa-07/driver/front-steer-right.png',
  'public/assets/characters/aa-07/driver/front-hit.png',
  'public/assets/characters/aa-07/driver/front-victory.png',
  'public/assets/characters/aa-08/driver/front-steer-left.png',
  'public/assets/characters/aa-08/driver/front-steer-right.png',
  'public/assets/characters/aa-08/driver/front-hit.png',
  'public/assets/characters/aa-08/driver/front-victory.png',
  'public/assets/characters/aa-11/driver/front.png',
  'public/assets/characters/aa-11/driver/front-steer-left.png',
  'public/assets/characters/aa-11/driver/front-steer-right.png',
  'public/assets/characters/aa-11/driver/front-hit.png',
  'public/assets/characters/aa-11/driver/front-victory.png',
  'public/assets/characters/aa-03/driver/front-steer-left.png',
  'public/assets/characters/aa-03/driver/front-steer-right.png',
  'public/assets/characters/aa-03/driver/front-hit.png',
  'public/assets/characters/aa-03/driver/front-victory.png',
]);

const kriosHornApertureFronts = new Set([
  'public/assets/characters/aa-10/driver/front-steer-left.png',
  'public/assets/characters/aa-10/driver/front-steer-right.png',
  'public/assets/characters/aa-10/driver/front-victory.png',
]);

const accuApertureRects = {
  'steer-left.png': [90, 225, 128, 261],
  'steer-right.png': [371, 199, 424, 230],
  'victory.png': [86, 293, 119, 321],
};

const mcfleurdelSteeringMatteRects = {
  'front-steer-left.png': [
    [65, 175, 131, 271],
    [315, 265, 386, 391],
  ],
  'front-steer-right.png': [
    [90, 200, 126, 301],
    [140, 365, 181, 401],
  ],
};

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

  if (newTransparentFronts.has(path)) {
    const decoded = decodeRgbaRows(pixels, width, height);
    const corners = [0, width - 1, (height - 1) * width, width * height - 1];
    if (corners.some((pixel) => decoded[pixel * 4 + 3] !== 0)) {
      throw new Error(`${path} must have transparent corners after checkerboard removal.`);
    }
  }

  if (kriosHornApertureFronts.has(path)) {
    const decoded = decodeRgbaRows(pixels, width, height);
    const hornApertures = countEnclosedTransparentRegions(decoded, width, height, 400);
    if (hornApertures < 2) {
      throw new Error(
        `${path} must preserve two transparent enclosed horn apertures; found ${String(hornApertures)}.`,
      );
    }
  }

  if (path.includes('/aa-11/driver/')) {
    const filename = path.split('/').at(-1);
    const aperture = accuApertureRects[filename];
    if (aperture !== undefined) {
      const decoded = decodeRgbaRows(pixels, width, height);
      let residualBackground = 0;
      for (let y = aperture[1]; y < aperture[3]; y += 1) {
        for (let x = aperture[0]; x < aperture[2]; x += 1) {
          const offset = (y * width + x) * 4;
          const red = decoded[offset];
          const green = decoded[offset + 1];
          const blue = decoded[offset + 2];
          const alpha = decoded[offset + 3];
          if (
            alpha > 0 &&
            Math.min(red, green, blue) >= 185 &&
            Math.max(red, green, blue) - Math.min(red, green, blue) <= 35
          ) {
            residualBackground += 1;
          }
        }
      }
      if (residualBackground > 0) {
        throw new Error(
          `${path} retains ${String(residualBackground)} opaque neutral checker pixels in its steering-wheel aperture.`,
        );
      }
    }
  }

  if (path.includes('/aa-07/driver/front-steer-')) {
    const filename = path.split('/').at(-1);
    const rects = mcfleurdelSteeringMatteRects[filename];
    if (rects !== undefined) {
      const decoded = decodeRgbaRows(pixels, width, height);
      const largestMatteComponent = largestPaleNeutralComponentInRects(
        decoded,
        width,
        height,
        rects,
      );
      if (largestMatteComponent >= 30) {
        throw new Error(
          `${path} retains a ${String(largestMatteComponent)}-pixel pale matte component in an approved transparent hair or arm gap.`,
        );
      }
    }
  }

  if (path.includes('/aa-03/')) {
    const decoded = decodeRgbaRows(pixels, width, height);
    const filename = path.split('/').at(-1);
    const protectedRect = lulaProtectedRects[filename];
    let residualBackground = 0;
    for (let y = 0; y < height; y += 1) {
      for (let x = 0; x < width; x += 1) {
        const offset = (y * width + x) * 4;
        const red = decoded[offset];
        const green = decoded[offset + 1];
        const blue = decoded[offset + 2];
        const alpha = decoded[offset + 3];
        const protectedPixel =
          protectedRect !== undefined &&
          x >= protectedRect[0] &&
          y >= protectedRect[1] &&
          x < protectedRect[2] &&
          y < protectedRect[3];
        if (
          !protectedPixel &&
          alpha > 0 &&
          Math.min(red, green, blue) >= 220 &&
          Math.max(red, green, blue) - Math.min(red, green, blue) <= 25
        ) {
          residualBackground += 1;
        }
      }
    }
    if (residualBackground > 0) {
      throw new Error(
        `${path} retains ${String(residualBackground)} opaque neutral-white background pixels.`,
      );
    }
  }
}

console.log(`Decoded and verified ${String(runtimePngs.length)} runtime character PNGs.`);
