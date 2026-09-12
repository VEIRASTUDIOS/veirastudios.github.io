/**
 * VEIRA STUDIOS — 2D Pixel Art Showcase: Rukia Audi RS6
 * - Clean showcase with background removed, letting just the car PNG display.
 * - When car is NOT selected (OFF): Stays stationary as an idle PNG.
 * - When car is selected (ON): Vibrates / shakes with dual-frequency engine idle rumble and suspension breathing.
 */

(function() {
  'use strict';

  class RukiaAudiDrive {
    constructor(canvasId) {
      this.canvas = document.getElementById(canvasId);
      if (!this.canvas) return;

      this.ctx = this.canvas.getContext('2d');
      this.carImg = new Image();
      this.carImg.src = 'rukia_audi_driving.png';
      this.carLoaded = false;
      this.carImg.onload = () => {
        this.carLoaded = true;
      };

      this.isVisible = true;

      // Car ignition power state (false = idle stationary PNG, true = shaking engine ON)
      this.isCarOn = false;

      // Throttle rev micro-surge
      this.revLift = 0;
      this.revIntensity = 0;

      // Headlight lighting state
      this.headlightAlpha = 0;
      this.headlightIgnitionTimer = 0;

      // Real Supercar V8 Sound System
      this.soundStart = new Audio('supercar_start.wav');
      this.soundStart.preload = 'auto';
      this.soundLoop = new Audio('supercar_loop.wav');
      this.soundLoop.preload = 'auto';
      this.soundLoop.loop = false; // Plays sound through and then automatically turns off
      this.soundStop = new Audio('supercar_stop.wav');
      this.soundStop.preload = 'auto';

      this.soundStart.volume = 0.90;
      this.soundLoop.volume = 0.75;
      this.soundStop.volume = 0.70;

      // When startup sequence finishes, play the engine sound
      this.soundStart.addEventListener('ended', () => {
        if (this.isCarOn && this.soundLoop) {
          this.soundLoop.currentTime = 0;
          this.soundLoop.play().catch(() => {});
        }
      });

      // When the engine sound reaches its end, automatically turn car OFF on its own
      this.soundLoop.addEventListener('ended', () => {
        if (this.isCarOn) {
          this.setCarPower(false);
        }
      });

      this.resize();
      window.addEventListener('resize', () => this.resize());

      this.setupInteractivity();
      this.setupVisibilityObserver();
      this.updateUI();

      this.lastTime = performance.now();
      this.animate = this.animate.bind(this);
      requestAnimationFrame(this.animate);
    }

    setCarPower(on) {
      const wasOn = this.isCarOn;
      this.isCarOn = !!on;

      if (this.isCarOn && !wasOn) {
        this.revIntensity = 1.0;
        this.headlightIgnitionTimer = 0.35; // Xenon strike arc flash

        // Play real supercar startup sound and schedule loop
        try {
          if (this.soundStop) {
            this.soundStop.pause();
            this.soundStop.currentTime = 0;
          }
          if (this.soundLoop) {
            this.soundLoop.pause();
            this.soundLoop.currentTime = 0;
          }
          if (this.soundStart) {
            this.soundStart.currentTime = 0;
            this.soundStart.play().catch(() => {});
          }
        } catch (e) {}
      } else if (!this.isCarOn && wasOn) {
        // Stop engine and play deceleration sound
        try {
          if (this.soundStart) {
            this.soundStart.pause();
            this.soundStart.currentTime = 0;
          }
          if (this.soundLoop) {
            this.soundLoop.pause();
            this.soundLoop.currentTime = 0;
          }
          if (this.soundStop) {
            this.soundStop.currentTime = 0;
            this.soundStop.play().catch(() => {});
          }
        } catch (e) {}
      }

      this.updateUI();
    }

    toggleCarPower() {
      this.setCarPower(!this.isCarOn);
      return this.isCarOn;
    }

    updateUI() {
      const btn = document.getElementById('car-ignition-btn');
      if (btn) {
        if (this.isCarOn) {
          btn.classList.add('car-on');
          btn.innerHTML = 'TURN CAR OFF';
        } else {
          btn.classList.remove('car-on');
          btn.innerHTML = 'TURN CAR ON';
        }
      }
    }

    resize() {
      const rect = this.canvas.parentElement.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.width = rect.width || 760;
      this.height = Math.max(360, Math.min(460, rect.width * 0.52));

      this.canvas.width = this.width * dpr;
      this.canvas.height = this.height * dpr;
      this.canvas.style.width = this.width + 'px';
      this.canvas.style.height = this.height + 'px';

      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.ctx.imageSmoothingEnabled = false;
    }

    setupInteractivity() {
      // Toggle car on click
      this.canvas.addEventListener('click', () => {
        this.toggleCarPower();
      });
    }

    setupVisibilityObserver() {
      if (!('IntersectionObserver' in window)) return;
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          this.isVisible = entry.isIntersecting;
        });
      }, { threshold: 0.05 });
      observer.observe(this.canvas);
    }

    update(dt, time) {
      if (this.isCarOn) {
        // Headlights fade in smoothly
        this.headlightAlpha = Math.min(1.0, this.headlightAlpha + dt * 4.5);
        if (this.headlightIgnitionTimer > 0) {
          this.headlightIgnitionTimer = Math.max(0, this.headlightIgnitionTimer - dt);
        }

        // Decay rev surge
        if (this.revIntensity > 0) {
          this.revIntensity = Math.max(0, this.revIntensity - dt * 2.2);
          this.revLift = Math.sin(time * 48) * (2.2 * this.revIntensity);
        } else {
          this.revLift = 0;
        }
      } else {
        // Headlights fade out smoothly
        this.headlightAlpha = Math.max(0, this.headlightAlpha - dt * 5.5);
        this.headlightIgnitionTimer = 0;
        this.revIntensity = 0;
        this.revLift = 0;
      }
    }

    // Effective headlight intensity including Xenon ignition strike & engine vibration hum
    getHeadlightIntensity(time) {
      if (this.headlightAlpha <= 0.002) return 0;
      let intensity = this.headlightAlpha;
      if (this.headlightIgnitionTimer > 0) {
        // High-intensity Xenon bulb arc ignition strike & micro-settle
        const prog = this.headlightIgnitionTimer / 0.35;
        intensity *= (1.0 + Math.sin(prog * Math.PI * 3.5) * 0.40 + prog * 0.30);
      }
      if (this.isCarOn) {
        // Realistic alternator luminescence micro-modulation synced with engine rumble
        intensity *= (1.0 + Math.sin(time * 58) * 0.025 + Math.cos(time * 84) * 0.015);
      }
      return Math.max(0, Math.min(1.85, intensity));
    }

    render(time) {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Clear canvas to complete transparency - NO background
      ctx.clearRect(0, 0, w, h);

      // Draw Audi RS6 PNG (idle or shaking) + active headlights effects
      this.drawRukiaAudi(ctx, w, h, time);
    }

    drawRukiaAudi(ctx, w, h, time) {
      const isWide = w >= 660;
      const carX = isWide ? Math.round(w * 0.34) : Math.round(w * 0.50);

      const carScale = Math.min(1.22, Math.max(0.85, w / 720));
      const carWidth = 240 * carScale;
      const carHeight = 240 * carScale;

      let vibY = 0;
      let chassisMicroRoll = 0;
      let breatheY = 0;
      let totalBounce = 0;

      // When selected (car is ON), the car starts to shake as now
      if (this.isCarOn) {
        const engineFreq = 34 + (this.revIntensity * 28);
        vibY = Math.sin(time * engineFreq) * 0.85 + Math.cos(time * 24) * 0.35;
        chassisMicroRoll = Math.sin(time * 40) * 0.0022;
        breatheY = Math.sin(time * 2.3) * 1.15;
        totalBounce = vibY + breatheY + this.revLift;
      }
      // When NOT selected, all offsets are 0 -> stays clean idle PNG!

      // Center car vertically
      const carBaseY = Math.round((h - carHeight) * 0.50);
      const carY = carBaseY + totalBounce;

      const headlightIntensity = this.getHeadlightIntensity(time);

      // Clean ground shadow right under the tires (no round glowing light effects under wheels)
      ctx.save();
      ctx.fillStyle = 'rgba(0, 0, 0, 0.60)';
      ctx.beginPath();
      const shadowRadius = carWidth * 0.46;
      ctx.ellipse(carX, carY + carHeight * 0.88, shadowRadius, 10, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // Draw Audi Sprite PNG and Headlights mounted in lockstep with chassis
      if (this.carLoaded) {
        ctx.save();
        ctx.translate(carX, carY + carHeight * 0.5);
        if (this.isCarOn) {
          ctx.rotate(chassisMicroRoll);
        }

        // 1. Car PNG sprite
        ctx.drawImage(
          this.carImg,
          -carWidth * 0.5,
          -carHeight * 0.5,
          carWidth,
          carHeight
        );

        // 2. Active headlights effects locked to car coordinates (kept exclusively on the headlights)
        if (headlightIntensity > 0.005) {
          this.drawHeadlightEffects(ctx, carWidth, carHeight, headlightIntensity, time, carScale);
        }

        ctx.restore();
      }
    }

    // High-fidelity Audi RS6 Headlights: Matrix DRLs, Xenon Projectors, Lens Flares & Halos
    drawHeadlightEffects(ctx, carWidth, carHeight, intensity, time, carScale) {
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';

      // Headlight Projector positions (normalized to car center):
      // Left: (-0.3359 * carWidth, 0.1328 * carHeight)
      // Right: (+0.3359 * carWidth, 0.1328 * carHeight)
      const lights = [
        { isRight: false, hx: -0.3359 * carWidth, hy: 0.1328 * carHeight, sign: -1 },
        { isRight: true,  hx:  0.3359 * carWidth, hy: 0.1328 * carHeight, sign:  1 }
      ];

      // Normalized vertices for Audi RS6 headlight casing polygon
      const polyNorm = [
        [ 0.4414, 0.0898 ],
        [ 0.3711, 0.0977 ],
        [ 0.2461, 0.1367 ],
        [ 0.2617, 0.1563 ],
        [ 0.3828, 0.1523 ],
        [ 0.4414, 0.1172 ]
      ];

      lights.forEach(light => {
        const { hx, hy, sign, isRight } = light;

        // 1. Headlight Housing Polygon (precise Audi RS6 casing)
        ctx.beginPath();
        polyNorm.forEach(([nx, ny], idx) => {
          const vx = sign * nx * carWidth;
          const vy = ny * carHeight;
          if (idx === 0) ctx.moveTo(vx, vy);
          else ctx.lineTo(vx, vy);
        });
        ctx.closePath();

        // Subtle internal xenon luminescence
        ctx.fillStyle = `rgba(6, 182, 212, ${0.25 * intensity})`;
        ctx.fill();

        // Crisp illuminated LED edge contour
        ctx.lineWidth = Math.max(1, 1.4 * carScale);
        ctx.strokeStyle = `rgba(224, 247, 250, ${0.75 * intensity})`;
        ctx.shadowColor = '#00f0ff';
        ctx.shadowBlur = 12 * carScale * intensity;
        ctx.stroke();
        ctx.shadowBlur = 0;

        // 2. Audi Matrix LED Segmented DRL Stripes along top slant
        const dRLCount = 6;
        for (let i = 0; i < dRLCount; i++) {
          const t = i / (dRLCount - 1);
          const sx = sign * (0.375 - t * 0.115) * carWidth;
          const sy1 = (0.098 + t * 0.036) * carHeight;
          const sy2 = sy1 + 0.020 * carHeight;

          ctx.beginPath();
          ctx.moveTo(sx, sy1);
          ctx.lineTo(sx, sy2);
          ctx.strokeStyle = `rgba(255, 255, 255, ${0.92 * intensity})`;
          ctx.lineWidth = Math.max(1.2, 1.8 * carScale);
          ctx.stroke();
        }

        // 3. Broad Atmospheric Luminous Bloom / Halo
        const bloomRadius = carWidth * 0.20;
        const bloom = ctx.createRadialGradient(hx, hy, 0, hx, hy, bloomRadius);
        bloom.addColorStop(0.0, `rgba(255, 255, 255, ${0.80 * intensity})`);
        bloom.addColorStop(0.20, `rgba(186, 230, 253, ${0.55 * intensity})`);
        bloom.addColorStop(0.50, `rgba(56, 189, 248, ${0.25 * intensity})`);
        bloom.addColorStop(0.80, `rgba(14, 116, 144, ${0.08 * intensity})`);
        bloom.addColorStop(1.0, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = bloom;
        ctx.beginPath();
        ctx.arc(hx, hy, bloomRadius, 0, Math.PI * 2);
        ctx.fill();

        // 4. Blinding Projector Core Hotspot
        const coreRadius = carWidth * 0.052;
        const core = ctx.createRadialGradient(hx, hy, 0, hx, hy, coreRadius);
        core.addColorStop(0.0, `rgba(255, 255, 255, ${Math.min(1.0, intensity * 1.3)})`);
        core.addColorStop(0.35, `rgba(240, 253, 255, ${0.95 * intensity})`);
        core.addColorStop(0.70, `rgba(125, 211, 252, ${0.65 * intensity})`);
        core.addColorStop(1.0, 'rgba(56, 189, 248, 0)');
        ctx.fillStyle = core;
        ctx.beginPath();
        ctx.arc(hx, hy, coreRadius, 0, Math.PI * 2);
        ctx.fill();

        // 5. Anamorphic Horizontal Lens Flare Streak
        const flareW = carWidth * 0.26;
        const flareH = carHeight * 0.015;
        const flare = ctx.createRadialGradient(hx, hy, 0, hx, hy, flareW);
        flare.addColorStop(0.0, `rgba(255, 255, 255, ${0.95 * intensity})`);
        flare.addColorStop(0.25, `rgba(186, 230, 253, ${0.75 * intensity})`);
        flare.addColorStop(0.60, `rgba(56, 189, 248, ${0.35 * intensity})`);
        flare.addColorStop(1.0, 'rgba(2, 132, 199, 0)');
        ctx.fillStyle = flare;
        ctx.beginPath();
        ctx.ellipse(hx, hy, flareW, flareH, isRight ? -0.04 : 0.04, 0, Math.PI * 2);
        ctx.fill();

        // 6. Cross Star Glint at projector core (shimmering with engine vibration)
        const glintRot = (time * 0.6) % (Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${0.75 * intensity})`;
        ctx.beginPath();
        ctx.ellipse(hx, hy, carWidth * 0.075, carHeight * 0.007, glintRot, 0, Math.PI * 2);
        ctx.ellipse(hx, hy, carWidth * 0.075, carHeight * 0.007, glintRot + Math.PI * 0.5, 0, Math.PI * 2);
        ctx.fill();
      });

      ctx.restore();
    }

    animate(timestamp) {
      requestAnimationFrame(this.animate);
      if (!this.isVisible) return;

      const dt = Math.min((timestamp - this.lastTime) / 1000, 0.1);
      this.lastTime = timestamp;
      const time = timestamp * 0.001;

      this.update(dt, time);
      this.render(time);
    }
  }

  // Robust initialization
  function initDrive() {
    if (document.getElementById('rukia-drive-canvas') && !window.rukiaDrive) {
      window.rukiaDrive = new RukiaAudiDrive('rukia-drive-canvas');
    }
  }

  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', initDrive);
  } else {
    setTimeout(initDrive, 10);
  }

})();
