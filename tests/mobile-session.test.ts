import { describe, expect, it, vi } from 'vitest';
import { isMobileSession, MOBILE_SESSION_QUERY } from '../src/app/mobileSession';

describe('mobile-session detection', () => {
  it('only enables touch controls for coarse no-hover input', () => {
    const matchMedia = vi.fn().mockReturnValue({ matches: true });
    expect(isMobileSession({ matchMedia } as unknown as Window)).toBe(true);
    expect(matchMedia).toHaveBeenCalledWith(MOBILE_SESSION_QUERY);
    matchMedia.mockReturnValue({ matches: false });
    expect(isMobileSession({ matchMedia } as unknown as Window)).toBe(false);
  });
});
