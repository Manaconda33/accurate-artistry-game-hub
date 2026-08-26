export type CharacterAssetState = 'production' | 'placeholder';

export interface CharacterStats {
  speed: number;
  acceleration: number;
  weight: number;
  handling: number;
  miniTurbo: number;
  traction: number;
}

export interface CharacterDefinition {
  id: string;
  displayName: string;
  descriptor: string;
  initials: string;
  accent: string;
  assetState: CharacterAssetState;
  portrait?: string;
  kart?: string;
  kartVisualYaw?: number;
  driverSpritePosition?: readonly [number, number, number];
  driver?: {
    rear: string;
    front?: string;
    steerLeft: string;
    steerRight: string;
    hit: string;
    victory: string;
  };
  stats: CharacterStats;
}

export const STAT_TOTAL = 36;
// Every production kart is authored and validated with glTF metadata
// `extras.forward: "-Z"`. KartMesh's chase-camera visual convention is the
// opposite, so the visual root must rotate PI without touching physics.
export const NEGATIVE_Z_KART_VISUAL_YAW = Math.PI;

export const LAVI_ASSET_REVISION = 'lavi-runtime-20260816-3';
export const MANACONDA_ASSET_REVISION = 'manaconda-runtime-20260820-1';
export const ACCU_ASSET_REVISION = 'accu-runtime-20260820-1';
export const KRAKEN_ASSET_REVISION = 'kraken-runtime-20260821-1';
export const CLEO_ASSET_REVISION = 'cleo-runtime-20260821-1';
export const KRIOS_ASSET_REVISION = 'krios-runtime-20260822-1';
export const KEEG_ASSET_REVISION = 'keeg-runtime-20260826-1';

const assetUrl = (path: string, revision: string): string =>
  `${import.meta.env.BASE_URL}${path}?v=${revision}`;

const lavi: CharacterDefinition = {
  id: 'aa-02',
  displayName: 'Lavi',
  descriptor: 'Feather Technician',
  initials: 'LV',
  accent: '#ef7f46',
  assetState: 'production',
  portrait: assetUrl('assets/characters/aa-02/portrait.png', LAVI_ASSET_REVISION),
  kart: assetUrl('assets/characters/aa-02/kart.glb', LAVI_ASSET_REVISION),
  kartVisualYaw: NEGATIVE_Z_KART_VISUAL_YAW,
  driver: {
    rear: assetUrl('assets/characters/aa-02/driver/rear.png', LAVI_ASSET_REVISION),
    steerLeft: assetUrl('assets/characters/aa-02/driver/steer-left.png', LAVI_ASSET_REVISION),
    steerRight: assetUrl('assets/characters/aa-02/driver/steer-right.png', LAVI_ASSET_REVISION),
    hit: assetUrl('assets/characters/aa-02/driver/hit.png', LAVI_ASSET_REVISION),
    victory: assetUrl('assets/characters/aa-02/driver/victory.png', LAVI_ASSET_REVISION),
  },
  stats: { speed: 5, acceleration: 8, weight: 2, handling: 9, miniTurbo: 8, traction: 4 },
};

const manaconda: CharacterDefinition = {
  id: 'aa-09',
  displayName: 'Manaconda',
  descriptor: 'Technical Cruiser',
  initials: 'MN',
  accent: '#5546c8',
  assetState: 'production',
  portrait: assetUrl('assets/characters/aa-09/portrait.png', MANACONDA_ASSET_REVISION),
  kart: assetUrl('assets/characters/aa-09/kart.glb', MANACONDA_ASSET_REVISION),
  kartVisualYaw: NEGATIVE_Z_KART_VISUAL_YAW,
  driver: {
    rear: assetUrl('assets/characters/aa-09/driver/rear.png', MANACONDA_ASSET_REVISION),
    steerLeft: assetUrl('assets/characters/aa-09/driver/steer-left.png', MANACONDA_ASSET_REVISION),
    steerRight: assetUrl(
      'assets/characters/aa-09/driver/steer-right.png',
      MANACONDA_ASSET_REVISION,
    ),
    hit: assetUrl('assets/characters/aa-09/driver/hit.png', MANACONDA_ASSET_REVISION),
    victory: assetUrl('assets/characters/aa-09/driver/victory.png', MANACONDA_ASSET_REVISION),
  },
  stats: { speed: 7, acceleration: 6, weight: 6, handling: 6, miniTurbo: 6, traction: 5 },
};

const accu: CharacterDefinition = {
  id: 'aa-11',
  displayName: 'Accu',
  descriptor: 'Perfect aim. Maximum armor.',
  initials: 'AC',
  accent: '#ec4d91',
  assetState: 'production',
  portrait: assetUrl('assets/characters/aa-11/portrait.png', ACCU_ASSET_REVISION),
  kart: assetUrl('assets/characters/aa-11/kart.glb', ACCU_ASSET_REVISION),
  kartVisualYaw: NEGATIVE_Z_KART_VISUAL_YAW,
  driver: {
    rear: assetUrl('assets/characters/aa-11/driver/rear.png', ACCU_ASSET_REVISION),
    steerLeft: assetUrl('assets/characters/aa-11/driver/steer-left.png', ACCU_ASSET_REVISION),
    steerRight: assetUrl('assets/characters/aa-11/driver/steer-right.png', ACCU_ASSET_REVISION),
    hit: assetUrl('assets/characters/aa-11/driver/hit.png', ACCU_ASSET_REVISION),
    victory: assetUrl('assets/characters/aa-11/driver/victory.png', ACCU_ASSET_REVISION),
  },
  stats: { speed: 8, acceleration: 4, weight: 10, handling: 3, miniTurbo: 5, traction: 6 },
};

const kraken: CharacterDefinition = {
  id: 'aa-05',
  displayName: 'Kraken',
  descriptor: 'Drift Specialist',
  initials: 'KR',
  accent: '#20d9e7',
  assetState: 'production',
  portrait: assetUrl('assets/characters/aa-05/portrait.png', KRAKEN_ASSET_REVISION),
  kart: assetUrl('assets/characters/aa-05/kart.glb', KRAKEN_ASSET_REVISION),
  kartVisualYaw: NEGATIVE_Z_KART_VISUAL_YAW,
  driver: {
    rear: assetUrl('assets/characters/aa-05/driver/rear.png', KRAKEN_ASSET_REVISION),
    front: assetUrl('assets/characters/aa-05/driver/front.png', KRAKEN_ASSET_REVISION),
    steerLeft: assetUrl('assets/characters/aa-05/driver/steer-left.png', KRAKEN_ASSET_REVISION),
    steerRight: assetUrl('assets/characters/aa-05/driver/steer-right.png', KRAKEN_ASSET_REVISION),
    hit: assetUrl('assets/characters/aa-05/driver/hit.png', KRAKEN_ASSET_REVISION),
    victory: assetUrl('assets/characters/aa-05/driver/victory.png', KRAKEN_ASSET_REVISION),
  },
  stats: { speed: 6, acceleration: 7, weight: 5, handling: 6, miniTurbo: 9, traction: 3 },
};

// Cleo is intentionally retained as a complete archived definition so her
// approved package can be restored without reconstructing paths, placement, or
// tuning. She is not included in characterManifest and therefore cannot be
// selected by the player or sampled into an AI grid.
export const archivedCleo: CharacterDefinition = {
  id: 'aa-06',
  displayName: 'Cleo',
  descriptor: 'Steady hands. Flawless lines.',
  initials: 'CL',
  accent: '#d79a35',
  assetState: 'production',
  portrait: assetUrl('assets/characters/aa-06/portrait.png', CLEO_ASSET_REVISION),
  kart: assetUrl('assets/characters/aa-06/kart.glb', CLEO_ASSET_REVISION),
  kartVisualYaw: NEGATIVE_Z_KART_VISUAL_YAW,
  driverSpritePosition: [0, 0.9, -0.72],
  driver: {
    rear: assetUrl('assets/characters/aa-06/driver/rear.png', CLEO_ASSET_REVISION),
    front: assetUrl('assets/characters/aa-06/driver/front.png', CLEO_ASSET_REVISION),
    steerLeft: assetUrl('assets/characters/aa-06/driver/steer-left.png', CLEO_ASSET_REVISION),
    steerRight: assetUrl('assets/characters/aa-06/driver/steer-right.png', CLEO_ASSET_REVISION),
    hit: assetUrl('assets/characters/aa-06/driver/hit.png', CLEO_ASSET_REVISION),
    victory: assetUrl('assets/characters/aa-06/driver/victory.png', CLEO_ASSET_REVISION),
  },
  stats: { speed: 6, acceleration: 6, weight: 5, handling: 7, miniTurbo: 5, traction: 7 },
};

const krios: CharacterDefinition = {
  id: 'aa-10',
  displayName: 'Krios',
  descriptor: 'Straight-Line Heavy',
  initials: 'KI',
  accent: '#d63b24',
  assetState: 'production',
  portrait: assetUrl('assets/characters/aa-10/portrait.png', KRIOS_ASSET_REVISION),
  kart: assetUrl('assets/characters/aa-10/kart.glb', KRIOS_ASSET_REVISION),
  kartVisualYaw: NEGATIVE_Z_KART_VISUAL_YAW,
  driver: {
    rear: assetUrl('assets/characters/aa-10/driver/rear.png', KRIOS_ASSET_REVISION),
    front: assetUrl('assets/characters/aa-10/driver/front.png', KRIOS_ASSET_REVISION),
    steerLeft: assetUrl('assets/characters/aa-10/driver/steer-left.png', KRIOS_ASSET_REVISION),
    steerRight: assetUrl('assets/characters/aa-10/driver/steer-right.png', KRIOS_ASSET_REVISION),
    hit: assetUrl('assets/characters/aa-10/driver/hit.png', KRIOS_ASSET_REVISION),
    victory: assetUrl('assets/characters/aa-10/driver/victory.png', KRIOS_ASSET_REVISION),
  },
  stats: { speed: 10, acceleration: 4, weight: 9, handling: 3, miniTurbo: 4, traction: 6 },
};

const keeg: CharacterDefinition = {
  id: 'aa-04',
  displayName: 'Keeg',
  descriptor: 'Balanced Racer',
  initials: 'KE',
  accent: '#8f4de8',
  assetState: 'production',
  portrait: assetUrl('assets/characters/aa-04/portrait.png', KEEG_ASSET_REVISION),
  kart: assetUrl('assets/characters/aa-04/kart.glb', KEEG_ASSET_REVISION),
  kartVisualYaw: NEGATIVE_Z_KART_VISUAL_YAW,
  driver: {
    rear: assetUrl('assets/characters/aa-04/driver/rear.png', KEEG_ASSET_REVISION),
    front: assetUrl('assets/characters/aa-04/driver/front.png', KEEG_ASSET_REVISION),
    steerLeft: assetUrl('assets/characters/aa-04/driver/steer-left.png', KEEG_ASSET_REVISION),
    steerRight: assetUrl('assets/characters/aa-04/driver/steer-right.png', KEEG_ASSET_REVISION),
    hit: assetUrl('assets/characters/aa-04/driver/hit.png', KEEG_ASSET_REVISION),
    victory: assetUrl('assets/characters/aa-04/driver/victory.png', KEEG_ASSET_REVISION),
  },
  stats: { speed: 7, acceleration: 7, weight: 5, handling: 7, miniTurbo: 5, traction: 5 },
};

export const characterManifest: readonly CharacterDefinition[] = [
  lavi,
  manaconda,
  accu,
  kraken,
  krios,
  keeg,
  ...[
    ['aa-01', 'AA 01', 'Balanced Pilot', 'A1', '#9b7cff', [6, 6, 6, 6, 6, 6]],
    ['aa-03', 'AA 03', 'Grip Specialist', 'A3', '#58c6a8', [5, 6, 5, 8, 5, 7]],
    ['aa-06', 'AA 06', 'Grip Specialist', 'A6', '#d79a35', [6, 6, 5, 7, 5, 7]],
    ['aa-07', 'AA 07', 'Top-Speed Ace', 'A7', '#b76be2', [9, 4, 6, 5, 5, 7]],
    ['aa-08', 'AA 08', 'Off-Road Scout', 'A8', '#79b84a', [6, 5, 6, 5, 6, 8]],
    ['aa-12', 'AA 12', 'Momentum Driver', '12', '#d56b55', [8, 5, 8, 4, 5, 6]],
  ].map(([id, displayName, descriptor, initials, accent, values]) => {
    const [speed, acceleration, weight, handling, miniTurbo, traction] = values as [
      number,
      number,
      number,
      number,
      number,
      number,
    ];
    return {
      id: id as string,
      displayName: displayName as string,
      descriptor: descriptor as string,
      initials: initials as string,
      accent: accent as string,
      assetState: 'placeholder' as const,
      stats: { speed, acceleration, weight, handling, miniTurbo, traction },
    };
  }),
];

export function validateCharacterManifest(
  manifest: readonly CharacterDefinition[] = characterManifest,
): string[] {
  const errors: string[] = [];
  if (manifest.length !== 12)
    errors.push(`Expected 12 characters; found ${String(manifest.length)}.`);
  const ids = new Set<string>();
  for (const character of manifest) {
    if (ids.has(character.id)) errors.push(`Duplicate character id: ${character.id}.`);
    ids.add(character.id);
    const values = statValues(character.stats);
    if (values.some((value) => !Number.isInteger(value) || value < 1 || value > 10)) {
      errors.push(`${character.id} has a stat outside the 1-10 range.`);
    }
    const total = values.reduce((sum, value) => sum + value, 0);
    if (total !== STAT_TOTAL)
      errors.push(`${character.id} totals ${String(total)}, not ${String(STAT_TOTAL)}.`);
    if (
      character.assetState === 'production' &&
      character.kart !== undefined &&
      character.kartVisualYaw !== NEGATIVE_Z_KART_VISUAL_YAW
    ) {
      errors.push(`${character.id} production kart must use the enforced negative-Z visual yaw.`);
    }
  }
  return errors;
}

export function characterById(id: string): CharacterDefinition {
  return characterManifest.find((character) => character.id === id) ?? lavi;
}

export function statValues(stats: CharacterStats): number[] {
  return [
    stats.speed,
    stats.acceleration,
    stats.weight,
    stats.handling,
    stats.miniTurbo,
    stats.traction,
  ];
}
