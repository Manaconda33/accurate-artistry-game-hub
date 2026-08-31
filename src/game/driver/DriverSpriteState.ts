export type DriverFrame = 'rear' | 'front' | 'steerLeft' | 'steerRight' | 'hit' | 'victory';

export interface DriverSpriteState {
  finished: boolean;
  hitSeconds: number;
  rearView: boolean;
  steering: number;
}

export function selectDriverFrame(state: DriverSpriteState): DriverFrame {
  if (state.finished) return 'victory';
  if (state.hitSeconds > 0) return 'hit';
  if (state.rearView) return 'front';
  if (state.steering > 0.15) return 'steerLeft';
  if (state.steering < -0.15) return 'steerRight';
  return 'rear';
}
