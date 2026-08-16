export const MOBILE_SESSION_QUERY = '(hover: none) and (pointer: coarse)';

export function isMobileSession(target: Window = window): boolean {
  return target.matchMedia(MOBILE_SESSION_QUERY).matches;
}
