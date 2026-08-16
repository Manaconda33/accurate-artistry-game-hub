import { describe, expect, it } from 'vitest';
import { RaceDirector, rankRacers, type RacerProgress } from '../src/game/race/RaceDirector';

function racer(id: string, lap: number, trackProgress: number): RacerProgress {
  return { id, lap, trackProgress, finished: false, finishTime: null, finishPlace: null };
}

describe('competitive race direction', () => {
  it('counts down before exposing race time', () => {
    const race = new RaceDirector();
    expect(race.countdownLabel()).toBe('3');
    race.advance(2.1);
    expect(race.countdownLabel()).toBe('1');
    expect(race.phase(false)).toBe('countdown');
    race.advance(0.9);
    expect(race.phase(false)).toBe('racing');
    expect(race.countdownLabel()).toBe('GO!');
    expect(race.raceTime()).toBeCloseTo(0);
  });

  it('ranks validated lap progress and locks finish placement', () => {
    const race = new RaceDirector(0);
    const racers = [racer('player', 1, 0.8), racer('ai-1', 2, 0.1), racer('ai-2', 1, 0.9)];
    expect(rankRacers(racers).map(({ id }) => id)).toEqual(['ai-1', 'ai-2', 'player']);
    const player = racers[0];
    const third = racers[2];
    if (player === undefined || third === undefined) throw new Error('Missing test racers');
    race.registerFinish(player);
    race.registerFinish(player);
    race.registerFinish(third);
    expect(racers[0]?.finishPlace).toBe(1);
    expect(racers[2]?.finishPlace).toBe(2);
  });
});
