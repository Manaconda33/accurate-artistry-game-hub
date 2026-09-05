from pathlib import Path

path = Path('src/game/KartTimeTrial.ts')
text = path.read_text()


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'Expected one anchor, found {count}: {old[:80]!r}')
    text = text.replace(old, new, 1)

replace_once(
    "import { createTrackScene } from './track/createTrackScene';\n",
    "import { createTrackScene } from './track/createTrackScene';\n"
    "import { ItemBoxSystem } from './items/ItemBoxSystem';\n"
    "import { ItemInventory } from './items/ItemInventory';\n"
    "import { selectItem } from './items/ItemSelector';\n"
    "import type { RaceRank } from './items/itemDefinitions';\n",
)

replace_once(
    "  private readonly track = new CircuitAlpha();\n  private readonly minimapTrack = normalizeMinimapTrack(this.track.samples);\n",
    "  private readonly track = new CircuitAlpha();\n"
    "  private readonly trackLength = this.track.curve.getLength();\n"
    "  private readonly minimapTrack = normalizeMinimapTrack(this.track.samples);\n",
)

replace_once(
    "  private readonly contactCooldowns = new Map<string, number>();\n",
    "  private readonly contactCooldowns = new Map<string, number>();\n"
    "  private readonly itemBoxes: ItemBoxSystem;\n"
    "  private readonly itemInventories = new Map<string, ItemInventory>();\n"
    "  private lastApexSelectionTime = Number.NEGATIVE_INFINITY;\n",
)

replace_once(
    "    this.chaseCamera = new ChaseCamera(this.camera);\n    this.scene.add(createTrackScene(this.track));\n",
    "    this.chaseCamera = new ChaseCamera(this.camera);\n"
    "    this.scene.add(createTrackScene(this.track));\n"
    "    this.itemBoxes = new ItemBoxSystem(this.track);\n"
    "    this.scene.add(this.itemBoxes.group);\n",
)

replace_once(
    "    window.removeEventListener('resize', this.resize);\n    this.renderer.dispose();\n",
    "    window.removeEventListener('resize', this.resize);\n"
    "    this.itemBoxes.dispose();\n"
    "    this.renderer.dispose();\n",
)

replace_once(
    "    this.playerProgress.trackProgress =\n      snapshot.lap === 0 && snapshot.nextCheckpoint === 1 && projection.progress > 0.8\n        ? 0\n        : projection.progress;\n    if (this.playerProgress.finished && !this.finishReported) {\n",
    "    this.playerProgress.trackProgress =\n"
    "      snapshot.lap === 0 && snapshot.nextCheckpoint === 1 && projection.progress > 0.8\n"
    "        ? 0\n"
    "        : projection.progress;\n"
    "    this.updateItemBoxes(dt);\n"
    "    if (this.playerProgress.finished && !this.finishReported) {\n",
)

methods = '''  private itemInventory(racerId: string): ItemInventory {
    const existing = this.itemInventories.get(racerId);
    if (existing !== undefined) return existing;
    const inventory = new ItemInventory();
    this.itemInventories.set(racerId, inventory);
    return inventory;
  }

  private updateItemBoxes(dt: number): void {
    const racers = [
      {
        id: 'player',
        position: this.kart.position(),
        finished: this.playerProgress.finished,
        canCollect: !this.itemInventory('player').isOccupied(),
      },
      ...this.opponents.map((opponent) => ({
        id: opponent.id,
        position: opponent.controller.position(),
        finished: opponent.progress.finished,
        canCollect: !this.itemInventory(opponent.id).isOccupied(),
      })),
    ];

    this.itemBoxes.update(dt, racers, ({ racerId }) => {
      const inventory = this.itemInventory(racerId);
      if (inventory.isOccupied()) return false;

      const standings = this.currentStandings();
      const racerIndex = standings.findIndex(({ id }) => id === racerId);
      const racer = standings[racerIndex];
      const leader = standings[0];
      if (racerIndex < 0 || racer === undefined || leader === undefined || racer.finished) return false;

      const rank = Math.min(8, Math.max(1, racerIndex + 1)) as RaceRank;
      const racerTotal = racer.lap + racer.trackProgress;
      const leaderTotal = leader.lap + leader.trackProgress;
      const distanceBehindLeaderMeters = Math.max(0, (leaderTotal - racerTotal) * this.trackLength);
      const apexAvailable = this.elapsed - this.lastApexSelectionTime >= 18;
      const itemId = selectItem({ rank, distanceBehindLeaderMeters, apexAvailable });
      if (!inventory.acquire(itemId)) return false;
      if (itemId === 'apex-missile') this.lastApexSelectionTime = this.elapsed;
      return true;
    });
  }

'''
replace_once("  private respawn(): void {\n", methods + "  private respawn(): void {\n")

path.write_text(text)
