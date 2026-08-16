import RAPIER from '@dimforge/rapier3d-compat';
import * as THREE from 'three';
import { Howler } from 'howler';
import { createKartTuning, sliceOneDriver, type SurfaceType } from '../config/kartTuning';
import { ChaseCamera } from './camera/ChaseCamera';
import { FixedStepRunner } from './physics/FixedStepRunner';
import { KartController, type DriveInput } from './physics/KartController';
import type { DriftTier } from './physics/KartController';
import { LapTracker } from './race/LapTracker';
import { CircuitAlpha } from './track/CircuitAlpha';
import { createTrackScene } from './track/createTrackScene';

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
}

export interface TimeTrialOptions {
  canvas: HTMLCanvasElement;
  onHud: (state: HudState) => void;
  onFinish: (time: number) => void;
}

export class KartTimeTrial {
  private readonly renderer: THREE.WebGLRenderer;
  private readonly scene = new THREE.Scene();
  private readonly camera: THREE.PerspectiveCamera;
  private readonly track = new CircuitAlpha();
  private readonly lapTracker = new LapTracker();
  private readonly fixedStep = new FixedStepRunner();
  private readonly pressed = new Set<string>();
  private readonly kartMesh = new THREE.Group();
  private readonly driftLights: THREE.Mesh[] = [];
  private readonly kart: KartController;
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

  public static async create(options: TimeTrialOptions): Promise<KartTimeTrial> {
    await RAPIER.init();
    return new KartTimeTrial(options);
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
      createKartTuning(sliceOneDriver),
      sliceOneDriver,
      spawn,
      yaw,
    );
    this.createKartVisual();
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

  private readonly frame = (now: number): void => {
    const frameSeconds = Math.min((now - this.lastFrame) / 1000, 0.1);
    this.lastFrame = now;
    if (!this.paused) {
      this.fixedStep.advance(frameSeconds, this.simulate);
      this.elapsed += frameSeconds;
    }

    this.updateVisuals(frameSeconds);
    this.renderer.render(this.scene, this.camera);
    this.updateHud(frameSeconds);
    this.animationFrame = requestAnimationFrame(this.frame);
  };

  private readonly simulate = (dt: number): void => {
    const position = this.kart.position(this.position);
    const projection = this.track.project(position);
    const input: DriveInput = {
      throttle: this.isPressed('KeyW', 'ArrowUp')
        ? 1
        : this.isPressed('KeyS', 'ArrowDown')
          ? -1
          : 0,
      steering: this.isPressed('KeyA', 'ArrowLeft')
        ? 1
        : this.isPressed('KeyD', 'ArrowRight')
          ? -1
          : 0,
      brake: false,
      drift: this.isPressed('Space'),
    };

    this.kart.update(input, projection.surface, dt);
    this.world.step();

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
      if (this.lapTracker.snapshot().finished) this.options.onFinish(this.elapsed);
    }
    this.lastCheckpointOverlap = checkpoint;
  };

  private nearestCheckpoint(position: THREE.Vector3): number {
    for (let index = 0; index < this.track.checkpointIndices.length; index += 1) {
      if (position.distanceToSquared(this.track.checkpointPosition(index)) < 13 * 13) return index;
    }
    return -1;
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
    this.chaseCamera.update(position, forward, this.pressed.has('KeyC'), dt);
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
      this.playTierTone(feedback.driftTier);
    }
    this.lastToneTier = feedback.driftTier;
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
    });
  }

  private createKartVisual(): void {
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
    this.scene.add(this.kartMesh);
  }

  private playTierTone(tier: DriftTier): void {
    const context = Howler.ctx;
    if (context.state !== 'running') return;
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    const frequency = tier === 'purple' ? 880 : tier === 'orange' ? 660 : 480;
    oscillator.frequency.setValueAtTime(frequency, context.currentTime);
    oscillator.type = 'sine';
    gain.gain.setValueAtTime(0.0001, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.09, context.currentTime + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + 0.16);
    oscillator.connect(gain).connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + 0.18);
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
