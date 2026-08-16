export interface LapSnapshot {
  lap: number;
  nextCheckpoint: number;
  finished: boolean;
  lastLapTime: number | null;
}

export class LapTracker {
  private lap = 0;
  private nextCheckpoint = 1;
  private finished = false;
  private lapStartedAt = 0;
  private lastLapTime: number | null = null;

  public constructor(
    private readonly checkpointCount = 12,
    private readonly targetLaps = 3,
  ) {}

  public reset(now = 0): void {
    this.lap = 0;
    this.nextCheckpoint = 1;
    this.finished = false;
    this.lapStartedAt = now;
    this.lastLapTime = null;
  }

  public enterCheckpoint(index: number, forwardDot: number, now: number): boolean {
    if (this.finished || forwardDot <= 0.15) return false;

    if (index === 0 && this.nextCheckpoint === 0) {
      this.lap += 1;
      this.lastLapTime = now - this.lapStartedAt;
      this.lapStartedAt = now;
      this.nextCheckpoint = 1;
      this.finished = this.lap >= this.targetLaps;
      return true;
    }

    if (index === this.nextCheckpoint) {
      this.nextCheckpoint = index === this.checkpointCount - 1 ? 0 : index + 1;
      return true;
    }

    return false;
  }

  public snapshot(): LapSnapshot {
    return {
      lap: this.lap,
      nextCheckpoint: this.nextCheckpoint,
      finished: this.finished,
      lastLapTime: this.lastLapTime,
    };
  }
}
