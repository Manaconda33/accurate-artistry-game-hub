export interface RacerProgress {
  id: string;
  lap: number;
  trackProgress: number;
  finished: boolean;
  finishTime: number | null;
  finishPlace: number | null;
}

export type RacePhase = 'countdown' | 'racing' | 'finished';

export function rankRacers(racers: readonly RacerProgress[]): RacerProgress[] {
  return [...racers].sort((a, b) => {
    if (a.finishPlace !== null || b.finishPlace !== null) {
      if (a.finishPlace === null) return 1;
      if (b.finishPlace === null) return -1;
      return a.finishPlace - b.finishPlace;
    }
    return b.lap + b.trackProgress - (a.lap + a.trackProgress);
  });
}

export class RaceDirector {
  private elapsed = 0;
  private finishCount = 0;

  public constructor(private readonly countdownSeconds = 3) {}

  public advance(dt: number): void {
    this.elapsed += dt;
  }

  public phase(playerFinished: boolean): RacePhase {
    if (playerFinished) return 'finished';
    return this.elapsed < this.countdownSeconds ? 'countdown' : 'racing';
  }

  public raceTime(): number {
    return Math.max(0, this.elapsed - this.countdownSeconds);
  }

  public countdownLabel(): string {
    const remaining = this.countdownSeconds - this.elapsed;
    if (remaining <= 0 && remaining > -0.8) return 'GO!';
    if (remaining <= -0.8) return '';
    return String(Math.max(1, Math.ceil(remaining)));
  }

  public registerFinish(progress: RacerProgress): void {
    if (progress.finishPlace !== null) return;
    this.finishCount += 1;
    progress.finished = true;
    progress.finishPlace = this.finishCount;
    progress.finishTime = this.raceTime();
  }
}
