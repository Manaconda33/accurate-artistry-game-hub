export class FixedStepRunner {
  private accumulator = 0;

  public constructor(
    private readonly stepSeconds = 1 / 60,
    private readonly maxFrameSeconds = 0.1,
  ) {}

  public advance(frameSeconds: number, simulate: (dt: number) => void): number {
    this.accumulator += Math.min(Math.max(frameSeconds, 0), this.maxFrameSeconds);
    let steps = 0;

    while (this.accumulator >= this.stepSeconds) {
      simulate(this.stepSeconds);
      this.accumulator -= this.stepSeconds;
      steps += 1;
    }

    return steps;
  }

  public alpha(): number {
    return this.accumulator / this.stepSeconds;
  }
}
