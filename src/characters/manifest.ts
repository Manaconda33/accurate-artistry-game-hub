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
  driver?: {
    rear: string;
    steerLeft: string;
    steerRight: string;
    hit: string;
    victory: string;
  };
  stats: CharacterStats;
}

export const STAT_TOTAL = 36;

const assetUrl = (path: string): string => `${import.meta.env.BASE_URL}${path}`;

const lavi: CharacterDefinition = {
  id: 'aa-02',
  displayName: 'Lavi',
  descriptor: 'Feather Technician',
  initials: 'LV',
  accent: '#ef7f46',
  assetState: 'production',
  portrait: assetUrl('assets/characters/aa-02/portrait.png'),
  kart: assetUrl('assets/characters/aa-02/kart.glb'),
  driver: {
    rear: assetUrl('assets/characters/aa-02/driver/rear.png'),
    steerLeft: assetUrl('assets/characters/aa-02/driver/steer-left.png'),
    steerRight: assetUrl('assets/characters/aa-02/driver/steer-right.png'),
    hit: assetUrl('assets/characters/aa-02/driver/hit.png'),
    victory: assetUrl('assets/characters/aa-02/driver/victory.png'),
  },
  stats: { speed: 5, acceleration: 8, weight: 2, handling: 9, miniTurbo: 8, traction: 4 },
};

export const characterManifest: readonly CharacterDefinition[] = [
  lavi,
  ...[
    ['aa-01', 'AA 01', 'Balanced Pilot', 'A1', '#9b7cff', [6, 6, 6, 6, 6, 6]],
    ['aa-03', 'AA 03', 'Grip Specialist', 'A3', '#58c6a8', [5, 6, 5, 8, 5, 7]],
    ['aa-04', 'AA 04', 'Launch Expert', 'A4', '#f3b84b', [6, 9, 3, 7, 7, 4]],
    ['aa-05', 'AA 05', 'Corner Carver', 'A5', '#45a7e8', [5, 7, 4, 9, 7, 4]],
    ['aa-06', 'AA 06', 'Road Bruiser', 'A6', '#e45c75', [7, 4, 9, 4, 5, 7]],
    ['aa-07', 'AA 07', 'Top-Speed Ace', 'A7', '#b76be2', [9, 4, 6, 5, 5, 7]],
    ['aa-08', 'AA 08', 'Off-Road Scout', 'A8', '#79b84a', [6, 5, 6, 5, 6, 8]],
    ['aa-09', 'AA 09', 'Turbo Tactician', 'A9', '#ec769f', [6, 6, 4, 6, 9, 5]],
    ['aa-10', 'AA 10', 'Heavy Cruiser', '10', '#c9824e', [8, 3, 9, 4, 4, 8]],
    ['aa-11', 'AA 11', 'Technical All-Rounder', '11', '#4fc3cf', [6, 7, 5, 7, 6, 5]],
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
