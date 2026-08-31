export type DriverFrame = 'rear' | 'front' | 'steerLeft' | 'steerRight' | 'hit' | 'victory';

export interface DriverSpriteState {
  finished: boolean;
  frontFacingCamera: boolean;
  hitSeconds: number;
  steering: number;
}

export type LocalPosition3 = readonly [number, number, number];

interface HorizontalVector {
  x: number;
  z: number;
}

export function isDriverFrontFacingCamera(
  racerPosition: HorizontalVector,
  racerForward: HorizontalVector,
  cameraPosition: HorizontalVector,
): boolean {
  const toCameraX = cameraPosition.x - racerPosition.x;
  const toCameraZ = cameraPosition.z - racerPosition.z;
  return racerForward.x * toCameraX + racerForward.z * toCameraZ > 0;
}

export function selectDriverFrame(state: DriverSpriteState): DriverFrame {
  if (state.finished) return 'victory';
  if (state.hitSeconds > 0) return 'hit';
  if (state.frontFacingCamera) return 'front';
  if (state.steering > 0.15) return 'steerLeft';
  if (state.steering < -0.15) return 'steerRight';
  return 'rear';
}

export function shouldShowModeledSteeringControl(
  driverSpriteIncludesSteeringControl: boolean,
  frame: DriverFrame,
): boolean {
  return !driverSpriteIncludesSteeringControl || frame === 'front';
}

export function modeledSteeringControlPosition(
  frame: DriverFrame,
  defaultPosition: LocalPosition3,
  frontPosition?: LocalPosition3,
): LocalPosition3 {
  return frame === 'front' && frontPosition !== undefined ? frontPosition : defaultPosition;
}
