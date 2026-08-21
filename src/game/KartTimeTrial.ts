import RAPIER from '@dimforge/rapier3d-compat';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { Howler } from 'howler';
import { playDriftTierTone } from '../audio/driftTone';
import { createKartTuning, type SurfaceType } from '../config/kartTuning';
import { AiDriver } from './ai/AiDriver';
import { ChaseCamera } from './camera/ChaseCamera';
import { FixedStepRunner } from './physics/FixedStepRunner';
import { KartController, type DriveInput } from './physics/KartController';
import type { DriftTier } from './physics/KartController';
import { collisionImpulseShares } from './physics/KartCollision';
import { LapTracker } from './race/LapTracker';
import { RaceDirector, rankRacers, type RacerProgress } from './race/RaceDirector';
import { CircuitAlpha } from './track/CircuitAlpha';
import { createTrackScene } from './track/createTrackScene';
import { characterManifest, type CharacterDefinition } from '../characters/manifest';
import { selectAiRoster } from '../characters/raceRoster';

type DriverFrame = 'rear' | 'front' | 'steerLeft' | 'steerRight' | 'hit' | 'victory';

export interface HudState {
  lap: number;
  speedKph: number;
  elapsed: number;
  surface: SurfaceType;
  wrongWay: boolean;
  fps: number;
  frameMs: number;
  finished: boolean;
  driftTier: DriftTier;
  driftCharge: number;
  boostActive: boolean;
  airborne: boolean;
  position: number;
  countdown: string;
}

export interface RaceResult {
  time: number;
  place: number;
  standings: { name: string; place: number | null; time: number | null }[];
}

export interface TimeTrialOptions {
  canvas: HTMLCanvasElement;
  character: CharacterDefinition;
  onHud: (state: HudState) => void;
  onFinish: (result: RaceResult) => void;
}

interface AiRacer {
  id: string;
  name: string;
  controller: KartController;
  driver: AiDriver;
  mesh: THREE.Group;
  lapTracker: LapTracker;
  progress: RacerProgress;
  lastCheckpointOverlap: number;
  recoveryCooldown: number;
}

export class KartTimeTrial {
  private readonly renderer: THREE.WebGLRenderer;
  private readonly scene = new THREE.Scene();
  private readonly camera: THREE.PerspectiveCamera;
  private readonly track = new CircuitAlpha();
  private readonly lapTracker = new LapTracker();
  private readonly raceDirector = new RaceDirector();
  private readonly fixedStep = new FixedStepRunner();
  private readonly pressed = new Set<string>();
  private readonly kartMesh = new THREE.Group();
  private readonly driftLights: THREE.Mesh[] = [];
  private readonly kart: KartController;
  private readonly opponents: AiRacer[] = [];
  private readonly chaseCamera: ChaseCamera;
  private readonly position = new THREE.Vector3();
  private readonly forward = new THREE.Vector3();
  private readonly world: RAPIER.World;
  private animationFrame = 0;
  private lastFrame = performance.now();
  private elapsed = 0;
  private paused = false;
  private lastCheckpointOverlap = -1;
  private lastRecoveryIndex = 0;
  private wrongWaySeconds = 0;
  private outOfBoundsSeconds = 0;
  private fpsAccumulator = 0;
  private fpsFrames = 0;
  private fps = 60;
  private lastToneTier: DriftTier = 'none';
  private readonly touchPressed = new Set<string>();
  private readonly driverTextures = new Map<DriverFrame, THREE.Texture>();
  private driverSprite: THREE.Sprite | null = null;
  private activeDriverFrame: DriverFrame = 'rear';
  private driverHitSeconds = 0;
  private playerSteering = 0;
  private rearViewActive = false;
  private readonly playerProgress: RacerProgress = {
    id: 'player',
    lap: 0,
    trackProgress: 0,
    finished: false,
    finishTime: null,
    finishPlace: null,
  };
  private finishReported = false;
  private readonly contactCooldowns = new Map<string, number>();

  public static async create(options: TimeTrialOptions): Promise<KartTimeTrial> {
    await RAPIER.init();
    const game = new KartTimeTrial(options);
    await game.createKartVisual();
    return game;
  }

  private constructor(private readonly options: TimeTrialOptions) {
    this.renderer = new THREE.WebGLRenderer({ canvas: options.canvas, antialias: true });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.scene.background = new THREE.Color(0x8f718f);
    this.scene.fog = new THREE.Fog(0x9b7d97, 180, 650);

    this.camera = new THREE.PerspectiveCamera(62, 1, 0.1, 900);
    this.chaseCamera = new ChaseCamera(this.camera);
    this.scene.add(createTrackScene(this.track));
    this.scene.add(new THREE.HemisphereLight(0xcbb7ff, 0x263822, 2.1));
    const sun = new THREE.DirectionalLight(0xffe8c5, 2.4);
    sun.position.set(-120, 180, -80);
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.camera.left = -340;
    sun.shadow.camera.right = 340;
    sun.shadow.camera.top = 340;
    sun.shadow.camera.bottom = -340;
    this.scene.add(sun);

    this.world = new RAPIER.World({ x: 0, y: -18, z: 0 });
    this.world.timestep = 1 / 60;
    this.world.createCollider(
      RAPIER.ColliderDesc.cuboid(450, 0.1, 450).setTranslation(0, -0.12, 0).setFriction(1),
    );

    const spawn = this.track
      .checkpointPosition(0)
      .addScaledVector(this.track.checkpointTangent(0), 8);
    const spawnTangent = this.track.checkpointTangent(0);
    const yaw = Math.atan2(spawnTangent.x, spawnTangent.z);
    this.kart = new KartController(
      this.world,
      createKartTuning(options.character.stats),
      options.character.stats,
      spawn,
      yaw,
    );
    this.createOpponents(spawn, spawnTangent, yaw);
    this.lapTracker.reset(0);
    this.bindEvents();
    this.resize();
  }

  public start(): void {
    this.lastFrame = performance.now();
    this.animationFrame = requestAnimationFrame(this.frame);
  }

  public dispose(): void {
    cancelAnimationFrame(this.animationFrame);
    window.removeEventListener('keydown', this.onKeyDown);
    window.removeEventListener('keyup', this.onKeyUp);
    window.removeEventListener('resize', this.resize);
    this.renderer.dispose();
  }

  public setTouchControl(control: string, pressed: boolean): void {
    if (pressed) this.touchPressed.add(control);
    else this.touchPressed.delete(control);
    if (control === 'recover' && pressed) this.respawn();
  }

  private readonly frame = (now: number): void => {
    const frameSeconds = Math.min((now - this.lastFrame) / 1000, 0.1);
    this.lastFrame = now;
    if (!this.paused) {
      this.fixedStep.advance(frameSeconds, this.simulate);
      this.elapsed = this.raceDirector.raceTime();
    }

    this.updateVisuals(frameSeconds);
    this.renderer.render(this.scene, this.camera);
    this.updateHud(frameSeconds);
    this.animationFrame = requestAnimationFrame(this.frame);
  };

  private readonly simulate = (dt: number): void => {
    this.raceDirector.advance(dt);
    if (this.raceDirector.phase(this.playerProgress.finished) === 'countdown') {
      this.world.step();
      return;
    }
    const position = this.kart.position(this.position);
    const projection = this.track.project(position);
    const input: DriveInput = {
      throttle:
        this.isPressed('KeyW', 'ArrowUp') || this.touchPressed.has('accelerate')
          ? 1
          : this.isPressed('KeyS', 'ArrowDown') || this.touchPressed.has('brake')
            ? -1
            : 0,
      steering:
        this.isPressed('KeyA', 'ArrowLeft') || this.touchPressed.has('left')
          ? 1
          : this.isPressed('KeyD', 'ArrowRight') || this.touchPressed.has('right')
            ? -1
            : 0,
      brake: false,
      drift: this.isPressed('Space') || this.touchPressed.has('drift'),
    };
    this.playerSteering = input.steering;
    this.driverHitSeconds = Math.max(0, this.driverHitSeconds - dt);

    this.kart.update(input, projection.surface, dt);
    this.updateOpponents(dt);
    this.world.step();
    this.resolveKartContacts(dt);

    if (!this.kart.isFinite()) {
      this.respawn();
      return;
    }

    const forwardDot = this.kart.forward(this.forward).dot(projection.tangent);
    this.wrongWaySeconds = forwardDot < -0.35 ? this.wrongWaySeconds + dt : 0;
    this.outOfBoundsSeconds = projection.lateralDistance > 34 ? this.outOfBoundsSeconds + dt : 0;

    if (projection.lateralDistance < 10) this.lastRecoveryIndex = projection.index;
    if (this.outOfBoundsSeconds > 1 || position.y < -3) this.respawn();

    const checkpoint = this.nearestCheckpoint(position);
    if (checkpoint !== -1 && checkpoint !== this.lastCheckpointOverlap) {
      const accepted = this.lapTracker.enterCheckpoint(checkpoint, forwardDot, this.elapsed);
      if (accepted && checkpoint !== 0) {
        this.lastRecoveryIndex = this.track.checkpointIndices[checkpoint] ?? projection.index;
      }
      if (this.lapTracker.snapshot().finished)
        this.raceDirector.registerFinish(this.playerProgress);
    }
    this.lastCheckpointOverlap = checkpoint;
    const snapshot = this.lapTracker.snapshot();
    this.playerProgress.lap = snapshot.lap;
    this.playerProgress.trackProgress =
      snapshot.lap === 0 && snapshot.nextCheckpoint === 1 && projection.progress > 0.8
        ? 0
        : projection.progress;
    if (this.playerProgress.finished && !this.finishReported) {
      this.finishReported = true;
      const standings = this.currentStandings();
      this.options.onFinish({
        time: this.playerProgress.finishTime ?? this.elapsed,
        place:
          this.playerProgress.finishPlace ?? standings.findIndex(({ id }) => id === 'player') + 1,
        standings: standings.map((racer) => ({
          name:
            racer.id === 'player'
              ? 'YOU'
              : (this.opponents.find(({ id }) => id === racer.id)?.name ?? racer.id),
          place: racer.finishPlace,
          time: racer.finishTime,
        })),
      });
    }
  };

  private nearestCheckpoint(position: THREE.Vector3): number {
    for (let index = 0; index < this.track.checkpointIndices.length; index += 1) {
      if (position.distanceToSquared(this.track.checkpointPosition(index)) < 13 * 13) return index;
    }
    return -1;
  }

  private updateOpponents(dt: number): void {
    const playerTotal = this.playerProgress.lap + this.playerProgress.trackProgress;
    for (const opponent of this.opponents) {
      opponent.recoveryCooldown = Math.max(0, opponent.recoveryCooldown - dt);
      const position = opponent.controller.position();
      const projection = this.track.project(position);
      const snapshot = opponent.lapTracker.snapshot();
      const opponentTotal = snapshot.lap + projection.progress;
      const input = opponent.progress.finished
        ? { throttle: 0, steering: 0, brake: true, drift: false }
        : opponent.driver.input(
            position,
            opponent.controller.forward(),
            opponent.controller.speedMetersPerSecond(),
            playerTotal - opponentTotal,
          );
      opponent.controller.update(input, projection.surface, dt);

      const checkpoint = this.nearestCheckpoint(position);
      if (checkpoint !== -1 && checkpoint !== opponent.lastCheckpointOverlap) {
        const forwardDot = opponent.controller.forward().dot(projection.tangent);
        opponent.lapTracker.enterCheckpoint(checkpoint, forwardDot, this.raceDirector.raceTime());
      }
      opponent.lastCheckpointOverlap = checkpoint;
      const nextSnapshot = opponent.lapTracker.snapshot();
      opponent.progress.lap = nextSnapshot.lap;
      opponent.progress.trackProgress =
        nextSnapshot.lap === 0 && nextSnapshot.nextCheckpoint === 1 && projection.progress > 0.8
          ? 0
          : projection.progress;
      if (nextSnapshot.finished) this.raceDirector.registerFinish(opponent.progress);

      if ((projection.lateralDistance > 20 || position.y < -2) && opponent.recoveryCooldown === 0) {
        const tangent = projection.tangent;
        opponent.controller.respawn(
          projection.point.clone().addScaledVector(tangent, 3),
          Math.atan2(tangent.x, tangent.z),
        );
        opponent.recoveryCooldown = 1.5;
      }
    }
  }

  private resolveKartContacts(dt: number): void {
    for (const [key, remaining] of this.contactCooldowns) {
      const next = remaining - dt;
      if (next <= 0) this.contactCooldowns.delete(key);
      else this.contactCooldowns.set(key, next);
    }

    const racers = [
      { id: 'player', controller: this.kart },
      ...this.opponents.map(({ id, controller }) => ({ id, controller })),
    ];
    for (let first = 0; first < racers.length; first += 1) {
      for (let second = first + 1; second < racers.length; second += 1) {
        const a = racers[first];
        const b = racers[second];
        if (a === undefined || b === undefined) continue;
        const key = `${a.id}:${b.id}`;
        if (this.contactCooldowns.has(key)) continue;
        const delta = a.controller.position().sub(b.controller.position()).setY(0);
        if (delta.lengthSq() >= 2.35 * 2.35 || delta.lengthSq() < 0.001) continue;
        const direction = delta.normalize();
        const impulses = collisionImpulseShares(a.controller.mass(), b.controller.mass(), 55);
        a.controller.applyArcadeCollisionImpulse(direction, impulses.first);
        b.controller.applyArcadeCollisionImpulse(direction.multiplyScalar(-1), impulses.second);
        if (a.id === 'player' || b.id === 'player') this.driverHitSeconds = 0.32;
        this.contactCooldowns.set(key, 0.18);
      }
    }
  }

  private currentStandings(): RacerProgress[] {
    return rankRacers([this.playerProgress, ...this.opponents.map(({ progress }) => progress)]);
  }

  private respawn(): void {
    const index = this.lastRecoveryIndex % this.track.sampleCount;
    const point = this.track.samples[index]?.clone() ?? this.track.checkpointPosition(0);
    const tangent = this.track.tangents[index]?.clone() ?? this.track.checkpointTangent(0);
    this.kart.respawn(point.addScaledVector(tangent, 4), Math.atan2(tangent.x, tangent.z));
    this.outOfBoundsSeconds = 0;
  }

  private updateVisuals(dt: number): void {
    const position = this.kart.position(this.position);
    const forward = this.kart.forward(this.forward);
    this.kartMesh.position.copy(position);
    this.kartMesh.rotation.y = Math.atan2(forward.x, forward.z);
    this.rearViewActive = this.pressed.has('KeyC') || this.touchPressed.has('rear');
    this.chaseCamera.update(position, forward, this.rearViewActive, dt);
    for (const opponent of this.opponents) {
      const opponentPosition = opponent.controller.position();
      const opponentForward = opponent.controller.forward();
      opponent.mesh.position.copy(opponentPosition);
      opponent.mesh.rotation.y = Math.atan2(opponentForward.x, opponentForward.z);
    }
    const feedback = this.kart.feedback();
    const color =
      feedback.driftTier === 'purple'
        ? 0xa855f7
        : feedback.driftTier === 'orange'
          ? 0xff8a28
          : 0x38bdf8;
    for (const light of this.driftLights) {
      light.visible = feedback.driftTier !== 'none';
      (light.material as THREE.MeshBasicMaterial).color.setHex(color);
      light.scale.setScalar(0.75 + feedback.chargeRatio * 1.4);
    }
    if (feedback.driftTier !== this.lastToneTier && feedback.driftTier !== 'none') {
      const context = (Howler as unknown as { ctx?: AudioContext | null }).ctx;
      playDriftTierTone(feedback.driftTier, context);
    }
    this.lastToneTier = feedback.driftTier;
    this.updateDriverSprite();
  }

  private updateHud(frameSeconds: number): void {
    this.fpsAccumulator += frameSeconds;
    this.fpsFrames += 1;
    if (this.fpsAccumulator >= 0.5) {
      this.fps = this.fpsFrames / this.fpsAccumulator;
      this.fpsAccumulator = 0;
      this.fpsFrames = 0;
    }

    const projection = this.track.project(this.kart.position(this.position));
    const snapshot = this.lapTracker.snapshot();
    const feedback = this.kart.feedback();
    this.options.onHud({
      lap: Math.min(snapshot.lap + 1, 3),
      speedKph: Math.round(this.kart.speedMetersPerSecond() * 3.6),
      elapsed: this.elapsed,
      surface: projection.surface,
      wrongWay: this.wrongWaySeconds > 0.55,
      fps: Math.round(this.fps),
      frameMs: frameSeconds * 1000,
      finished: snapshot.finished,
      driftTier: feedback.driftTier,
      driftCharge: feedback.chargeRatio,
      boostActive: feedback.boostActive,
      airborne: feedback.airborne,
      position: this.currentStandings().findIndex(({ id }) => id === 'player') + 1,
      countdown: this.raceDirector.countdownLabel(),
    });
  }

  private async createKartVisual(): Promise<void> {
    if (this.options.character.kart !== undefined) {
      try {
        const gltf = await new GLTFLoader().loadAsync(this.options.character.kart);
        const model = gltf.scene;
        // Keep physics untouched and apply only the manifest's enforced
        // visual-axis correction. Production GLBs use `extras.forward: -Z`;
        // this visual root requires PI to face away from the chase camera.
        model.rotation.y = this.options.character.kartVisualYaw ?? 0;
        const bounds = new THREE.Box3().setFromObject(model);
        const size = bounds.getSize(new THREE.Vector3());
        const scale = 2.9 / Math.max(size.x, size.z, 0.001);
        model.scale.setScalar(scale);
        bounds.setFromObject(model);
        model.position.y = -bounds.min.y - 0.42;
        model.traverse((object) => {
          if (object instanceof THREE.Mesh) {
            object.castShadow = true;
            object.receiveShadow = true;
          }
        });
        this.kartMesh.add(model);
        this.addDriverSprite();
        this.addDriftLights();
        this.scene.add(this.kartMesh);
        return;
      } catch (error) {
        console.warn(
          `Could not load ${this.options.character.displayName}'s kart; using fallback.`,
          error,
        );
      }
    }
    this.createFallbackKartVisual();
    this.addDriverSprite();
  }

  private addDriverSprite(): void {
    const driver = this.options.character.driver;
    if (driver === undefined) return;
    const loader = new THREE.TextureLoader();
    const paths: Partial<Record<DriverFrame, string>> = {
      rear: driver.rear,
      front: driver.front,
      steerLeft: driver.steerLeft,
      steerRight: driver.steerRight,
      hit: driver.hit,
      victory: driver.victory,
    };
    const rearTexture = loader.load(driver.rear);
    rearTexture.colorSpace = THREE.SRGBColorSpace;
    this.driverTextures.set('rear', rearTexture);
    for (const [frame, path] of Object.entries(paths) as [DriverFrame, string | undefined][]) {
      if (frame === 'rear' || path === undefined) continue;
      loader.load(
        path,
        (texture) => {
          texture.colorSpace = THREE.SRGBColorSpace;
          this.driverTextures.set(frame, texture);
          if (this.activeDriverFrame === frame) this.applyDriverFrame(frame);
        },
        undefined,
        () => {
          console.warn(
            `Could not load ${this.options.character.displayName}'s ${frame} driver frame.`,
          );
        },
      );
    }
    const sprite = new THREE.Sprite(
      new THREE.SpriteMaterial({ map: rearTexture, transparent: true, depthWrite: false }),
    );
    sprite.name = 'DriverSprite';
    sprite.scale.set(1.45, 1.45, 1);
    sprite.position.set(0, 0.95, -0.12);
    this.kartMesh.add(sprite);
    this.driverSprite = sprite;
  }

  private updateDriverSprite(): void {
    if (this.driverSprite === null) return;
    const desired: DriverFrame = this.playerProgress.finished
      ? 'victory'
      : this.driverHitSeconds > 0
        ? 'hit'
        : this.rearViewActive
          ? 'front'
          : this.playerSteering > 0.15
            ? 'steerLeft'
            : this.playerSteering < -0.15
              ? 'steerRight'
              : 'rear';
    this.applyDriverFrame(desired);
  }

  private applyDriverFrame(frame: DriverFrame): void {
    const texture = this.driverTextures.get(frame) ?? this.driverTextures.get('rear');
    if (this.driverSprite === null || texture === undefined) return;
    const material = this.driverSprite.material;
    if (material.map !== texture) {
      material.map = texture;
      material.needsUpdate = true;
    }
    this.activeDriverFrame = frame;
  }

  private addDriftLights(): void {
    for (const x of [-0.72, 0.72]) {
      const spark = new THREE.Mesh(
        new THREE.SphereGeometry(0.16, 8, 6),
        new THREE.MeshBasicMaterial({ color: 0x38bdf8 }),
      );
      spark.position.set(x, -0.08, -1.15);
      spark.visible = false;
      this.driftLights.push(spark);
      this.kartMesh.add(spark);
    }
  }

  private createFallbackKartVisual(): void {
    const chassis = new THREE.Mesh(
      new THREE.BoxGeometry(1.5, 0.55, 2.45),
      new THREE.MeshStandardMaterial({ color: 0x63328b, metalness: 0.42, roughness: 0.3 }),
    );
    chassis.position.y = 0.15;
    chassis.castShadow = true;
    const nose = new THREE.Mesh(
      new THREE.BoxGeometry(1.15, 0.38, 0.85),
      new THREE.MeshStandardMaterial({ color: 0xe6b84f, metalness: 0.35, roughness: 0.32 }),
    );
    nose.position.set(0, 0.2, 1.18);
    nose.castShadow = true;
    this.kartMesh.add(chassis, nose);

    const wheelMaterial = new THREE.MeshStandardMaterial({ color: 0x121216, roughness: 0.9 });
    for (const x of [-0.82, 0.82]) {
      for (const z of [-0.72, 0.72]) {
        const wheel = new THREE.Mesh(
          new THREE.CylinderGeometry(0.31, 0.31, 0.25, 14),
          wheelMaterial,
        );
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, -0.12, z);
        wheel.castShadow = true;
        this.kartMesh.add(wheel);
      }
    }
    this.addDriftLights();
    this.scene.add(this.kartMesh);
  }

  private createOpponents(spawn: THREE.Vector3, tangent: THREE.Vector3, yaw: number): void {
    const right = new THREE.Vector3(tangent.z, 0, -tangent.x);
    const aiRoster = selectAiRoster(characterManifest, this.options.character.id, 7);
    for (let index = 0; index < 7; index += 1) {
      const character = aiRoster[index];
      if (character === undefined) continue;
      const row = Math.floor(index / 2) + 1;
      const side = index % 2 === 0 ? -1 : 1;
      const position = spawn
        .clone()
        .addScaledVector(tangent, -row * 3.2)
        .addScaledVector(right, side * 2.05);
      const stats = character.stats;
      const controller = new KartController(
        this.world,
        createKartTuning(stats),
        stats,
        position,
        yaw,
      );
      const mesh = this.createOpponentVisual(character);
      this.scene.add(mesh);
      this.opponents.push({
        id: `ai-${String(index + 1)}`,
        name: character.displayName,
        controller,
        driver: new AiDriver(this.track, {
          laneOffset: side * (0.7 + row * 0.35),
          pace: 0.28 + index * 0.09,
          aggression: 0.2 + (index % 4) * 0.2,
        }),
        mesh,
        lapTracker: new LapTracker(),
        progress: {
          id: `ai-${String(index + 1)}`,
          lap: 0,
          trackProgress: 0,
          finished: false,
          finishTime: null,
          finishPlace: null,
        },
        lastCheckpointOverlap: -1,
        recoveryCooldown: 0,
      });
    }
  }

  private createOpponentVisual(character: CharacterDefinition): THREE.Group {
    const group = new THREE.Group();
    if (character.kart !== undefined) {
      void new GLTFLoader().loadAsync(character.kart).then(
        (gltf) => {
          const model = gltf.scene;
          model.rotation.y = character.kartVisualYaw ?? 0;
          const bounds = new THREE.Box3().setFromObject(model);
          const size = bounds.getSize(new THREE.Vector3());
          model.scale.setScalar(2.9 / Math.max(size.x, size.z, 0.001));
          bounds.setFromObject(model);
          model.position.y = -bounds.min.y - 0.42;
          model.traverse((object) => {
            if (object instanceof THREE.Mesh) {
              object.castShadow = true;
              object.receiveShadow = true;
            }
          });
          group.clear();
          group.add(model);
          if (character.driver !== undefined) {
            const texture = new THREE.TextureLoader().load(character.driver.rear);
            texture.colorSpace = THREE.SRGBColorSpace;
            const sprite = new THREE.Sprite(
              new THREE.SpriteMaterial({ map: texture, transparent: true, depthWrite: false }),
            );
            sprite.scale.set(1.45, 1.45, 1);
            sprite.position.set(0, 0.95, -0.12);
            group.add(sprite);
          }
        },
        () => {
          console.warn(`Could not load AI kart for ${character.displayName}; using fallback.`);
        },
      );
    }
    const chassis = new THREE.Mesh(
      new THREE.BoxGeometry(1.45, 0.52, 2.35),
      new THREE.MeshStandardMaterial({
        color: new THREE.Color(character.accent),
        metalness: 0.25,
        roughness: 0.38,
      }),
    );
    chassis.position.y = 0.15;
    chassis.castShadow = true;
    const canopy = new THREE.Mesh(
      new THREE.BoxGeometry(0.85, 0.42, 0.75),
      new THREE.MeshStandardMaterial({ color: 0x201729, roughness: 0.5 }),
    );
    canopy.position.set(0, 0.55, -0.15);
    group.add(chassis, canopy);
    return group;
  }

  private bindEvents(): void {
    window.addEventListener('keydown', this.onKeyDown, { passive: false });
    window.addEventListener('keyup', this.onKeyUp, { passive: false });
    window.addEventListener('resize', this.resize);
  }

  private readonly onKeyDown = (event: KeyboardEvent): void => {
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(event.code)) {
      event.preventDefault();
    }
    if ((event.code === 'Escape' || event.code === 'KeyP') && !event.repeat) {
      this.paused = !this.paused;
    }
    if (event.code === 'KeyR' && !event.repeat) this.respawn();
    this.pressed.add(event.code);
  };

  private readonly onKeyUp = (event: KeyboardEvent): void => {
    this.pressed.delete(event.code);
  };

  private isPressed(...codes: string[]): boolean {
    return codes.some((code) => this.pressed.has(code));
  }

  private readonly resize = (): void => {
    const width = this.options.canvas.clientWidth || window.innerWidth;
    const height = this.options.canvas.clientHeight || window.innerHeight;
    this.camera.aspect = width / Math.max(height, 1);
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height, false);
  };
}
