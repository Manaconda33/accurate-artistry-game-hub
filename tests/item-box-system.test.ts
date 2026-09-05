import * as THREE from 'three';
import { describe, expect, it, vi } from 'vitest';
import { ItemBoxSystem, createItemBoxPlacements } from '../src/game/items/ItemBoxSystem';
import { ITEM_BOX_LAYOUT } from '../src/game/items/itemDefinitions';
import { CircuitAlpha } from '../src/game/track/CircuitAlpha';

function racerAt(position: THREE.Vector3, overrides: Partial<{ finished: boolean; canCollect: boolean }> = {}) {
  return {
    id: 'player',
    position: position.clone().setY(0),
    finished: overrides.finished ?? false,
    canCollect: overrides.canCollect ?? true,
  };
}

describe('Slice 5 visible item boxes', () => {
  it('places four rows of eight inside the legal Circuit Alpha road corridor', () => {
    const track = new CircuitAlpha();
    const placements = createItemBoxPlacements(track);

    expect(placements).toHaveLength(32);
    for (const rowProgress of ITEM_BOX_LAYOUT.rowProgress) {
      expect(placements.filter(({ progress }) => progress === rowProgress)).toHaveLength(8);
    }
    for (const placement of placements) {
      expect(Math.abs(placement.lateralOffset)).toBeLessThan(track.roadHalfWidth);
      const projected = track.project(placement.position.clone().setY(0));
      expect(projected.lateralDistance).toBeLessThan(track.roadHalfWidth);
    }
  });

  it('renders one named visual for each governed placement', () => {
    const system = new ItemBoxSystem(new CircuitAlpha());

    expect(system.group.name).toBe('slice-5-item-boxes');
    expect(system.group.children).toHaveLength(32);
    expect(system.group.getObjectByName('item-box-0')).toBeDefined();
    expect(system.group.getObjectByName('item-box-31')).toBeDefined();

    system.dispose();
  });

  it('accepts the closest eligible racer and immediately starts the pop phase', () => {
    const system = new ItemBoxSystem(new CircuitAlpha());
    const placement = system.placements[0];
    expect(placement).toBeDefined();
    if (placement === undefined) return;
    const onCollection = vi.fn(() => true);

    system.update(1 / 60, [racerAt(placement.position)], onCollection);

    expect(onCollection).toHaveBeenCalledOnce();
    expect(onCollection).toHaveBeenCalledWith({
      boxIndex: 0,
      row: 0,
      column: 0,
      racerId: 'player',
    });
    expect(system.presentation(0)?.phase).toBe('popping');
    expect(system.presentation(0)?.collectible).toBe(false);

    system.dispose();
  });

  it('does not consume a box for a finished or occupied racer', () => {
    const system = new ItemBoxSystem(new CircuitAlpha());
    const placement = system.placements[0];
    expect(placement).toBeDefined();
    if (placement === undefined) return;
    const onCollection = vi.fn(() => true);

    system.update(1 / 60, [racerAt(placement.position, { canCollect: false })], onCollection);
    system.update(1 / 60, [racerAt(placement.position, { finished: true })], onCollection);

    expect(onCollection).not.toHaveBeenCalled();
    expect(system.presentation(0)?.phase).toBe('available');
    expect(system.presentation(0)?.collectible).toBe(true);

    system.dispose();
  });

  it('keeps a rejected collection available for another valid racer', () => {
    const system = new ItemBoxSystem(new CircuitAlpha());
    const placement = system.placements[0];
    expect(placement).toBeDefined();
    if (placement === undefined) return;
    const rejected = vi.fn(() => false);

    system.update(1 / 60, [racerAt(placement.position)], rejected);

    expect(rejected).toHaveBeenCalledOnce();
    expect(system.presentation(0)?.phase).toBe('available');
    expect(system.presentation(0)?.collectible).toBe(true);

    system.dispose();
  });

  it('shows hidden then fade-back phases before becoming collectible again', () => {
    const system = new ItemBoxSystem(new CircuitAlpha());
    const placement = system.placements[0];
    expect(placement).toBeDefined();
    if (placement === undefined) return;

    system.update(1 / 60, [racerAt(placement.position)], () => true);
    system.update(0.2, [], () => false);
    expect(system.presentation(0)?.phase).toBe('hidden');
    expect(system.presentation(0)?.visible).toBe(false);

    system.update(3.9, [], () => false);
    expect(system.presentation(0)?.phase).toBe('respawning');
    expect(system.presentation(0)?.visible).toBe(true);
    expect(system.presentation(0)?.collectible).toBe(false);
    expect(system.presentation(0)?.opacity).toBeGreaterThan(0);
    expect(system.presentation(0)?.opacity).toBeLessThan(1);

    system.update(0.5, [], () => false);
    expect(system.presentation(0)?.phase).toBe('available');
    expect(system.presentation(0)?.collectible).toBe(true);
    expect(system.presentation(0)?.opacity).toBe(1);

    system.dispose();
  });
});
