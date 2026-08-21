import type { CharacterDefinition } from './manifest';

export type RandomSource = () => number;

export function selectAiRoster(
  roster: readonly CharacterDefinition[],
  playerId: string,
  count: number,
  random: RandomSource = Math.random,
): CharacterDefinition[] {
  const candidates = roster.filter(({ id }) => id !== playerId);
  if (count > candidates.length) throw new Error('AI roster exceeds the available unique racers.');

  for (let index = candidates.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(random() * (index + 1));
    const current = candidates[index];
    const swap = candidates[swapIndex];
    if (current !== undefined && swap !== undefined) {
      candidates[index] = swap;
      candidates[swapIndex] = current;
    }
  }
  return candidates.slice(0, count);
}
